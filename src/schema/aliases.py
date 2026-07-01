"""
aliases.py
=====================================

Canonical Alias Registry

Responsibilities
----------------
✓ Resolve semantically equivalent column names
✓ Convert normalized columns into canonical schema
✓ Remain independent of any specific data source

This module assumes all incoming column names have already
been processed by ColumnNormalizer.

Examples
--------
location                -> station
pm_2_5_avg              -> pm25
relative_humidity_2m    -> humidity
temperature_2m          -> temperature
wind_speed_10m          -> wind_speed
"""

from __future__ import annotations

from typing import Iterable


class AliasResolver:
    """
    Resolve normalized column names to canonical names.
    """

    # ======================================================
    # Canonical aliases
    # ======================================================

    ALIASES = {

    # ======================================================
    # Identity
    # ======================================================

    "serial": "serial",

    "station": "station",
    "location": "station",
    "station_name": "station",
    "station_id": "station",
    "site": "station",
    "site_name": "station",
    "monitoring_station": "station",

    "district": "district",

    "date": "date",
    "time": "time",
    "hour": "hour",
    "datetime": "datetime",

    "latitude": "latitude",
    "longitude": "longitude",

    "aqi": "aqi",

    # ======================================================
    # PM2.5
    # ======================================================

    "pm25": "pm25",
    "pm_25": "pm25",
    "pm_2_5": "pm25",
    "pm_2_5_avg": "pm25",
    "pm_2_5_average": "pm25",

    # ======================================================
    # PM10
    # ======================================================

    "pm10": "pm10",
    "pm_10": "pm10",
    "pm_10_avg": "pm10",
    "pm_10_average": "pm10",

    # ======================================================
    # Weather
    # ======================================================

    # Temperature
    "temperature": "temperature",
    "temperature_2m": "temperature",
    "temperature_2m_c": "temperature",

    # Humidity
    "humidity": "humidity",
    "relative_humidity": "humidity",
    "relative_humidity_2m": "humidity",
    "rel_humi": "humidity",

    # Dew Point
    "dew_point": "dew_point",
    "dew_point_2m": "dew_point",
    "dew_point_2m_c": "dew_point",

    # Pressure
    "pressure": "pressure",
    "surface_pressure": "pressure",

    # Precipitation
    "precipitation": "precipitation",

    # Cloud Cover
    "cloud_cover": "cloud_cover",

    # ======================================================
    # Wind Direction
    # ======================================================

    "wind_direction": "wind_direction",
    "wind_direction_avg": "wind_direction",
    "wind_direction_10m": "wind_direction",

    # ======================================================
    # Wind Speed
    # ======================================================

    "wind_speed": "wind_speed",
    "wind_speed_avg": "wind_speed",
    "wind_speed_10m": "wind_speed",
    "wind_speed_10m_km_h": "wind_speed",

    # ======================================================
    # Wind Speed Min
    # ======================================================

    "wind_speed_min": "wind_speed_min",
    "wind_speed_minimum": "wind_speed_min",
    "wind_speed_minimum_in_m_s": "wind_speed_min",

    # ======================================================
    # Wind Speed Max
    # ======================================================

    "wind_speed_max": "wind_speed_max",
    "wind_speed_maximum": "wind_speed_max",
    "wind_speed_maximum_in_m_s": "wind_speed_max",

    # ======================================================
    # Wind Gust
    # ======================================================

    "wind_gust": "wind_gust",
    "wind_gusts": "wind_gust",
    "wind_gust_10m": "wind_gust",
    "wind_gusts_10m": "wind_gust",
    "wind_gusts_10m_km_h": "wind_gust",
}

    # ======================================================

    @classmethod
    def resolve(cls, column: str) -> str:
        """
        Resolve one normalized column to its canonical name.

        Unknown columns are returned unchanged.
        """

        return cls.ALIASES.get(column, column)

    # ======================================================

    @classmethod
    def resolve_columns(
        cls,
        columns: Iterable[str],
    ) -> list[str]:
        """
        Resolve multiple normalized columns.
        """

        return [
            cls.resolve(column)
            for column in columns
        ]

    # ======================================================

    @classmethod
    def resolve_dataframe(cls, df):
        """
        Return a dataframe with canonical column names.
        """

        df = df.copy()

        df.columns = cls.resolve_columns(df.columns)

        return df

    # ======================================================

    @classmethod
    def register(
        cls,
        alias: str,
        canonical: str,
    ) -> None:
        """
        Register a new alias at runtime.

        Useful when onboarding a new stakeholder dataset.
        """

        cls.ALIASES[alias] = canonical

    # ======================================================

    @classmethod
    def available(cls) -> dict[str, str]:
        """
        Return all registered aliases.
        """

        return dict(sorted(cls.ALIASES.items()))