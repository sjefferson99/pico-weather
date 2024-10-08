from lib.ulogging import uLogger
from asyncio import Event, sleep, create_task
from time import time, gmtime
from config import UPLOAD_RETRY_SECONDS, MAX_UPLOADS_PER_MIN, DESTINATIONS
from lib.destinations.influxdb import InfluxDB
from lib.destinations.example import ExampleDestination

class WeatherData:
    """
    Register sensors for data gathering and upload watchers
    """
    def __init__(self) -> None:
        self.weather_data_payloads = []
        self.log = uLogger("WeatherData")
        self.log.info("Init Weather Data")
        self.data_ready = Event()
        self.cache_file = "weather_data_cache.txt"
        self.upload_retry_seconds = 60
        self.upload_retry_seconds = UPLOAD_RETRY_SECONDS
        self.max_upload_per_min = MAX_UPLOADS_PER_MIN
        self.InfluxDB = InfluxDB()
        self.Example = ExampleDestination()
        self.failed_readings = []
        self.UPLOAD_SUCCESS = 0
        self.UPLOAD_FAILED = 1

        # self.configure_destinations(DESTINATIONS)

    def startup(self) -> None:
        """
        Start data watchers
        """
        self.log.info("Starting Weather Data services")
        create_task(self.async_data_watcher())
        create_task(self.async_cached_data_manager())
    
    # def configure_destinations(self, destinations: list) -> None:
    #     self.destinations = []
    #     self.destination_objects = []
        
    #     for destination in destinations:
    #         try:
    #             destination_class = globals().get(destination)
                
    #             if destination_class is None:
    #                 raise ValueError(f"Destination class '{destination}' not found.")
                
    #             destination = destination_class()
    #             self.destination_objects.append(destination)
    #         except Exception as e:
    #             print(f"An error occurred while confguring destination '{destination}': {e}")
    #             raise
    
    async def async_data_watcher(self) -> None:
        """
        Watch for new data and upload not more frequently than max_upload_per_min.
        Cache data to file on upload failure.
        """
        while True:
            await self.data_ready.wait()
            self.log.info("Data ready to upload")
            self.data_ready.clear()
            try:
                failed_readings = await self.async_upload_payloads(self.weather_data_payloads)
                if len(failed_readings) > 0:
                    self.write_data_to_file(failed_readings)
            
            except Exception as e:
                self.log.error(f"Failed to upload data: {e}")
                self.write_data_to_file(self.weather_data_payloads)
            
            finally:
                self.weather_data_payloads = []
            
            await sleep(60 / self.max_upload_per_min)
    
    def write_data_to_file(self, data: list) -> None:
        """
        Append passed in data to cache file.
        """
        self.log.info(f"Writing data to file: {data}")
        with open(self.cache_file, "a") as cache:
            for entry in data:
                cache.write(str(entry) + "\n")
        self.log.info("Data written to file")

    async def async_cached_data_manager(self) -> None:
        """
        Look for cached data and regularly retry upload.
        re-cache any failed uploads.
        """
        while True:
            self.log.info("Checking for cached data")
            with open(self.cache_file, "r") as cache:
                cache_data = cache.read()

            if len(cache_data) > 0:
                try:
                    self.log.info("Found cached data, retrying upload")
                    data = []
                    for line in cache_data.split("\n"):
                        self.log.info(f"Reading line from file: {line}")
                        if line != "":
                            data.append(line)
                    self.log.info(f"cached data: {data}")
                    failed_readings = await self.async_upload_payloads(data)

                    if len(failed_readings) == len(data):
                        self.log.error("All cached data failed to upload")
                    else:
                        with open(self.cache_file, "w") as cache:
                            for reading in failed_readings:
                                cache.write(reading + "\n")
                        self.log.error(f"Some data failed to upload and has been re-cached: {failed_readings}")
                
                except Exception as e:
                    self.log.error(f"Failed to upload cached data: {e}")
            
            await sleep(self.upload_retry_seconds)

    async def async_upload_payloads(self, dataset: list) -> list:
        """
        Pass each set of readings in the dataset to the upload_readings method.
        Return any failed uploads for further processing.
        Dataset is a list of dicts {"destination": "<destination>, "data": {"timestamp": timestamp, "readings": {"key": value}}}
        """
        self.log.info(f"Uploading all payloads: {dataset}")
        failed_uploads = []
        for payload in dataset:
            self.log.info(f"Uploading payload: {payload["data"]} to {payload["destination"]}")
            result = await self.async_upload_payload(payload["data"], payload["destination"])
            if result == self.UPLOAD_FAILED:
                self.log.error(f"Failed to upload payload: {payload}")
                failed_uploads.append(payload)
            else:
                self.log.info(f"Payload uploaded successfully: {payload}")
        
        self.log.info(f"Failed payload uploads (if any): {failed_uploads}")
        return failed_uploads
    
    async def async_upload_payload(self, data: dict, destination: str) -> int:
        """
        Pass readings to the target upload destination.
        Format: {"timestamp": timestamp, "readings": {"key": value}}
        """
        try:
            self.log.info(f"Uploading data: {data} to: {destination}")
            
            destination_object = getattr(self, destination, None)
            if destination_object is None:
                raise ValueError(f"Destination object '{destination}' not found.")

            result = await destination_object.async_upload_data(data)
            return result

        except Exception as e:
            self.log.error(f"Failed to upload payload: {e}")
            return self.UPLOAD_FAILED
    
    def add_readings(self, data: dict) -> None:
        """
        Add timestamp to suplied reading data and add to the upload queue for all configured destinations.
        """
        self.log.info(f"Adding readings: {data}")
        if gmtime()[0] < 2022:
            raise ValueError("Invalid timestamp")
        for destination in DESTINATIONS:
            readings = {"destination": destination, "data": {"timestamp": time(), "readings": data}}
            self.log.info(f"Readings added to upload queue as payload for destination: {readings}")
            self.weather_data_payloads.append(readings)
        self.data_ready.set()
