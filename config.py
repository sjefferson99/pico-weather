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

NTP_SYNC_INTERVAL_SECONDS = 86400

I2C_PINS = {"sda": 0, "scl": 1}

# Adjust daily rain day for UK BST
UK_BST = True

# For local time corrections to daily rain logging other than BST
# Ignored if uk_bst = True
UTC_OFFSET = 0

# where to upload to ("http", "mqtt", "adafruit_io", "influxdb", "wunderground")
DESTINATION = None
# Optional secondary destination
# set to None if not in use
SECONDARY_DESTINATION = None

# influxdb settings
INFLUXDB_ORG = ""
INFLUXDB_URL = ""
INFLUXDB_TOKEN = ""
INFLUXDB_BUCKET = ""
INFLUXDB_DEVICE = CUSTOM_HOSTNAME

# weather underground settings
WUNDERGROUND_STATION_ID = None
WUNDERGROUND_STATION_KEY = None

# height in metres above sea level for atmospheric pressure compensation
HEIGHT_ABOVE_SEA_LEVEL_M = 52

# offset up to +/- 360 degrees for wind direction if you can't reorientate the weather station
WIND_DIRECTION_OFFSET = 0

#BME280
BME280_POLL_FREQUENCY = 60

UPLOAD_RETRY_SECONDS = 30
