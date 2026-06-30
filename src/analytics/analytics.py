"""
analytics.py

DuckDB Analytics Engine

Responsibilities
----------------
1. Connect to DuckDB
2. Execute reusable SQL queries
3. Return results as Pandas DataFrames
4. Provide helper methods for common analytics
"""

from typing import Optional

import pandas as pd

from src.database.connection import get_connection
from src.analytics import queries


class AnalyticsEngine:
    """
    Generic DuckDB Analytics Engine.
    """

    def __init__(self):
        self.con = get_connection()

    # =====================================================
    # Generic Query Executor
    # =====================================================

    def query(self, sql: str) -> pd.DataFrame:
        """
        Execute any SQL query and return a DataFrame.
        """
        return self.con.execute(sql).fetchdf()

    # =====================================================
    # Master Datasets
    # =====================================================

    def environmental_master(self):
        return self.query(queries.ENVIRONMENTAL_MASTER)

    def realtime_environmental_master(self):
        return self.query(
            queries.REALTIME_ENVIRONMENTAL_MASTER
        )

    def wbpcb_master(self):
        return self.query(
            queries.WBPCB_MASTER
        )

    def weather_master(self):
        return self.query(
            queries.WEATHER_MASTER
        )

    # =====================================================
    # Metadata
    # =====================================================

    def dataset_count(self):
        return self.query(
            queries.DATASET_COUNTS
        )

    def station_list(self):
        return self.query(
            queries.STATION_LIST
        )

    def date_range(self):
        return self.query(
            queries.DATE_RANGE
        )

    # =====================================================
    # AQI Analytics
    # =====================================================

    def average_aqi_by_station(self):
        return self.query(
            queries.AVERAGE_AQI_BY_STATION
        )

    def daily_aqi(self):
        return self.query(
            queries.DAILY_AQI
        )

    def monthly_aqi(self):
        return self.query(
            queries.MONTHLY_AQI
        )

    # =====================================================
    # PM Analytics
    # =====================================================

    def daily_pm25(self):
        return self.query(
            queries.DAILY_PM25
        )

    def daily_pm10(self):
        return self.query(
            queries.DAILY_PM10
        )

    # =====================================================
    # Weather Analytics
    # =====================================================

    def temperature_trend(self):
        return self.query(
            queries.TEMPERATURE_TREND
        )

    def humidity_trend(self):
        return self.query(
            queries.HUMIDITY_TREND
        )

    # =====================================================
    # Correlation Dataset
    # =====================================================

    def aqi_weather(self):
        return self.query(
            queries.AQI_WEATHER
        )

    # =====================================================
    # Custom Query
    # =====================================================

    def custom_query(self, sql: str):
        """
        Execute any user-defined SQL query.
        """
        return self.query(sql)

    # =====================================================
    # Utility
    # =====================================================

    def close(self):
        """
        Close the DuckDB connection.
        """
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


if __name__ == "__main__":

    analytics = AnalyticsEngine()

    print("=" * 70)
    print("DuckDB Analytics Test")
    print("=" * 70)

    print("\nStations")
    print(analytics.station_list().head())

    print("\nDate Range")
    print(analytics.date_range())

    print("\nAverage AQI")
    print(analytics.average_aqi_by_station().head())

    analytics.close()