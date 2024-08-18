## Logging
# Level 0-4: 0 = Disabled, 1 = Critical, 2 = Error, 3 = Warning, 4 = Info
LOG_LEVEL = 2
# Handlers: Populate list with zero or more of the following log output handlers (case sensitive): "Console", "File"
LOG_HANDLERS = ["Console", "File"]
# Max log file size in bytes, there will be a maximum of 2 files at this size created
LOG_FILE_MAX_SIZE = 10240

## WIFI
WIFI_SSID = ""
WIFI_PASSWORD = ""
WIFI_COUNTRY = "GB"
WIFI_CONNECT_TIMEOUT_SECONDS = 10
WIFI_CONNECT_RETRIES = 1
WIFI_RETRY_BACKOFF_SECONDS = 5
# Leave as none for MAC based unique hostname or specify a custom hostname string
CUSTOM_HOSTNAME = "Pico-Weather"
# Upload frequency management
UPLOAD_RETRY_SECONDS = 30
MAX_UPLOADS_PER_MIN = 10

NTP_SYNC_INTERVAL_SECONDS = 86400

I2C_PINS = {"sda": 0, "scl": 1}

# Influxdb settings
INFLUXDB_ORG = ""
INFLUXDB_URL = ""
INFLUXDB_TOKEN = ""
INFLUXDB_BUCKET = ""
INFLUXDB_DEVICE = CUSTOM_HOSTNAME

# Weather underground settings
WUNDERGROUND_STATION_ID = None
WUNDERGROUND_STATION_KEY = None

# Height in metres above sea level for atmospheric pressure compensation
HEIGHT_ABOVE_SEA_LEVEL_M = 0

# BME280
BME280_POLL_FREQUENCY = 60

# Destination selection: Add one or more of the following to the list: "InfluxDB", "Example"
DESTINATIONS = ["InfluxDB", "Example"]
