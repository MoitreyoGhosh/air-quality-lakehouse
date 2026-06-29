"""
Expected schemas for all managed datasets.
"""

SCHEMAS = {

    "environmental_master": [

        "station_id",
        "station_name",
        "datetime",
        "aqi",
        "pm25",
        "pm10",
        "temperature_2m",
        "relative_humidity_2m",
        "dew_point_2m",
        "precipitation",
        "surface_pressure",
        "cloud_cover",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
        "latitude",
        "longitude",
        "year",
        "month",
        "hour"

    ],

    "wbpcb_master": [
        # Add WBPCB columns here
    ],

    "openmeteo_weather_master": [
        # Add weather dataset columns here
    ]

}