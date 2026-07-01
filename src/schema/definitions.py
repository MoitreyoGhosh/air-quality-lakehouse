"""
definitions.py

Default schema definitions for the Environmental
Intelligence Framework.

Each schema maps source column names to the
framework's standardized column names.

These mappings are used by SchemaMapper before
datasets enter the Lakehouse.

Future datasets only need a new schema dictionary.
"""

# ==========================================================
# WBPCB Historical AQI Dataset
# ==========================================================

WBPCB_SCHEMA = {

    # Date & Time
    "from date": "date",
    "to date": "date",
    "date": "date",
    "time": "time",

    # Station
    "station": "station",
    "station name": "station",

    # Air Quality
    "aqi": "aqi",
    "pm2.5": "pm25",
    "pm25": "pm25",
    "pm10": "pm10",

    "no": "no",
    "no2": "no2",
    "nox": "nox",
    "nh3": "nh3",
    "so2": "so2",
    "co": "co",
    "o3": "o3",

    # Coordinates
    "latitude": "latitude",
    "longitude": "longitude",
}

# ==========================================================
# Open-Meteo Historical Weather Dataset
# ==========================================================

OPENMETEO_SCHEMA = {

    "date": "date",
    "time": "time",

    "temperature_2m": "temperature",
    "relative_humidity_2m": "humidity",
    "dew_point_2m": "dew_point",

    "precipitation": "precipitation",
    "rain": "rain",
    "snowfall": "snowfall",

    "surface_pressure": "pressure",

    "cloud_cover": "cloud_cover",

    "wind_speed_10m": "wind_speed",

    "wind_direction_10m": "wind_direction",

    "wind_gusts_10m": "wind_gust",

    "shortwave_radiation": "solar_radiation",

    "station": "station",
}