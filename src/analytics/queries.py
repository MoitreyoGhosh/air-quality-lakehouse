"""
queries.py

Central SQL library for the Environmental Intelligence Lakehouse.

Every SQL query used by notebooks, dashboards, or reports
should be stored here.
"""

# ==========================================================
# MASTER TABLES
# ==========================================================

ENVIRONMENTAL_MASTER = """
SELECT *
FROM environmental_master
"""

REALTIME_ENVIRONMENTAL_MASTER = """
SELECT *
FROM realtime_environmental_master
"""

WBPCB_MASTER = """
SELECT *
FROM wbpcb_master
"""

WEATHER_MASTER = """
SELECT *
FROM weather_master
"""

# ==========================================================
# BASIC SUMMARY
# ==========================================================

DATASET_COUNTS = """
SELECT
    COUNT(*) AS total_records
FROM environmental_master
"""

STATION_LIST = """
SELECT DISTINCT
    station_name
FROM environmental_master
ORDER BY station_name
"""

DATE_RANGE = """
SELECT
    MIN(datetime) AS start_date,
    MAX(datetime) AS end_date
FROM environmental_master
"""

# ==========================================================
# AQI
# ==========================================================

AVERAGE_AQI_BY_STATION = """
SELECT
    station_name,
    AVG(aqi) AS average_aqi
FROM environmental_master
GROUP BY station_name
ORDER BY average_aqi DESC
"""

DAILY_AQI = """
SELECT
    DATE(datetime) AS date,
    AVG(aqi) AS average_aqi
FROM environmental_master
GROUP BY DATE(datetime)
ORDER BY date
"""

MONTHLY_AQI = """
SELECT
    YEAR(datetime) AS year,
    MONTH(datetime) AS month,
    AVG(aqi) AS average_aqi
FROM environmental_master
GROUP BY
    YEAR(datetime),
    MONTH(datetime)
ORDER BY
    year,
    month
"""

# ==========================================================
# PM2.5
# ==========================================================

DAILY_PM25 = """
SELECT
    DATE(datetime) AS date,
    AVG(pm25) AS average_pm25
FROM environmental_master
GROUP BY DATE(datetime)
ORDER BY date
"""

# ==========================================================
# PM10
# ==========================================================

DAILY_PM10 = """
SELECT
    DATE(datetime) AS date,
    AVG(pm10) AS average_pm10
FROM environmental_master
GROUP BY DATE(datetime)
ORDER BY date
"""

# ==========================================================
# WEATHER
# ==========================================================

TEMPERATURE_TREND = """
SELECT
    DATE(datetime) AS date,
    AVG(temperature_2m) AS average_temperature
FROM weather_master
GROUP BY DATE(datetime)
ORDER BY date
"""

HUMIDITY_TREND = """
SELECT
    DATE(datetime) AS date,
    AVG(relative_humidity_2m) AS average_humidity
FROM weather_master
GROUP BY DATE(datetime)
ORDER BY date
"""

WEATHER_SUMMARY = """
SELECT
    station_id,
    AVG(temperature_2m) AS average_temperature,
    AVG(relative_humidity_2m) AS average_humidity,
    AVG(surface_pressure) AS average_pressure,
    AVG(wind_speed_10m) AS average_wind_speed,
    AVG(wind_gusts_10m) AS average_wind_gusts
FROM weather_master
GROUP BY station_id
ORDER BY station_id
"""

# ==========================================================
# AQI + WEATHER
# ==========================================================

AQI_WEATHER = """
SELECT
    e.datetime,
    e.station_name,
    e.aqi,
    e.pm25,
    e.pm10,
    w.temperature_2m,
    w.relative_humidity_2m,
    w.surface_pressure,
    w.wind_speed_10m,
    w.wind_direction_10m,
    w.wind_gusts_10m
FROM environmental_master e
LEFT JOIN weather_master w
ON e.station_id = w.station_id
AND e.datetime = w.datetime
ORDER BY e.datetime
"""