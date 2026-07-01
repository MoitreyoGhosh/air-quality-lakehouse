"""
rules.py
=====================================

Validation Rule Definitions

This module defines reusable validation rules for
canonical environmental datasets.

The rules are generic and independent of any
specific connector or data source.

Responsibilities
----------------
✓ Required column definitions
✓ Numeric column definitions
✓ Coordinate ranges
✓ Pollutant constraints
✓ Weather constraints
✓ Null thresholds

Not Responsible For
-------------------
✗ Executing validation
✗ Reporting
✗ Data cleaning
"""

from __future__ import annotations


class ValidationRules:
    """
    Repository of validation rules.
    """

    # =====================================================
    # Required Columns
    # =====================================================

    REQUIRED_COLUMNS = {
        "wbpcb": [
            "station",
            "date",
            "hour",
            "latitude",
            "longitude",
            "aqi",
            "pm25",
            "pm10",
        ],
        "openmeteo": [
            "time",
            "temperature",
            "humidity",
        ],
    }

    # =====================================================
    # Numeric Columns
    # =====================================================

    NUMERIC_COLUMNS = {
        "wbpcb": [
            "aqi",
            "pm25",
            "pm10",
            "latitude",
            "longitude",
            "humidity",
            "temperature",
            "wind_speed",
            "wind_speed_min",
            "wind_speed_max",
        ],
        "openmeteo": [
            "temperature",
            "humidity",
            "dew_point",
            "precipitation",
            "pressure",
            "cloud_cover",
            "wind_speed",
            "wind_direction",
            "wind_gust",
        ],
    }

    # =====================================================
    # Coordinate Bounds
    # =====================================================

    LATITUDE_RANGE = (-90.0, 90.0)

    LONGITUDE_RANGE = (-180.0, 180.0)

    # =====================================================
    # Non-negative Measurements
    # =====================================================

    NON_NEGATIVE = [
        "aqi",
        "pm25",
        "pm10",
        "precipitation",
        "wind_speed",
        "wind_speed_min",
        "wind_speed_max",
        "wind_gust",
    ]

    # =====================================================
    # Percentage Columns
    # =====================================================

    PERCENTAGE_COLUMNS = {
        "humidity": (0, 100),
        "cloud_cover": (0, 100),
    }

    # =====================================================
    # Duplicate Keys
    # =====================================================

    DUPLICATE_KEYS = {
        "wbpcb": [
            "station",
            "date",
            "hour",
        ],
        "openmeteo": [
            "time",
        ],
    }

    # =====================================================
    # Null Threshold
    # =====================================================

    DEFAULT_NULL_THRESHOLD = 0.20

    # =====================================================
    # Access Helpers
    # =====================================================

    @classmethod
    def required_columns(cls, dataset_type: str) -> list[str]:
        """
        Return required columns for a dataset type.
        """
        return cls.REQUIRED_COLUMNS.get(dataset_type, [])

    @classmethod
    def numeric_columns(cls, dataset_type: str) -> list[str]:
        """
        Return numeric columns for a dataset type.
        """
        return cls.NUMERIC_COLUMNS.get(dataset_type, [])

    @classmethod
    def duplicate_keys(cls, dataset_type: str) -> list[str]:
        """
        Return duplicate key columns for a dataset type.
        """
        return cls.DUPLICATE_KEYS.get(dataset_type, [])