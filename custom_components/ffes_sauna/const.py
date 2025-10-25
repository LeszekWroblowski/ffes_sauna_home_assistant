"""Constants for the FFES Sauna integration."""

DOMAIN = "ffes_sauna"

# Configuration
CONF_HOST = "host"

# Default values
DEFAULT_SCAN_INTERVAL = 30

# API endpoints
ENDPOINT_DATA = "/sauna-data"
ENDPOINT_CONTROL = "/sauna-control"

# Sauna status values
STATUS_OFF = 0
STATUS_HEATING = 1
STATUS_VENTILATION = 2
STATUS_STANDBY = 3

STATUS_MAP = {
    STATUS_OFF: "off",
    STATUS_HEATING: "heating",
    STATUS_VENTILATION: "ventilation",
    STATUS_STANDBY: "standby",
}

# Sauna profiles
PROFILES = {
    1: "Infrared Sauna",
    2: "Dry Sauna",
    3: "Wet Sauna",
    4: "Ventilation",
    5: "Steambath",
    6: "Infrared CPIR",
    7: "Infrared MIX",
}

PROFILE_REVERSE_MAP = {v: k for k, v in PROFILES.items()}

# Temperature limits
MIN_TEMP = 20
MAX_TEMP = 110

# Humidity limits
MIN_HUMIDITY = 0
MAX_HUMIDITY = 100
