"""
test.py
=====================================

Realtime Pipeline Test

Tests
-----
✓ Station Metadata
✓ Weather API
✓ AQI API
✓ Single Station Ingestion
✓ Full Ingestion
"""

from __future__ import annotations

import pandas as pd

from src.realtime.fetcher import OpenMeteoFetcher
from src.realtime.ingestion import RealtimeIngestion


# ==========================================================
# Helpers
# ==========================================================

def divider() -> None:
    print("=" * 80)


def section(title: str) -> None:
    divider()
    print(title)
    divider()


def dataframe_summary(
    name: str,
    df: pd.DataFrame,
) -> None:

    print(f"\n{name}")

    print("-" * 80)

    print(f"Rows    : {len(df)}")

    print(f"Columns : {len(df.columns)}")

    if df.empty:
        print("Dataset is empty.")
        return

    print("\nColumns")

    print(list(df.columns))

    if "time" in df.columns:

        print(
            f"\nDatetime : "
            f"{df['time'].min()} -> {df['time'].max()}"
        )

    print("\nMissing Values")

    print(df.isna().sum())

    print("\nHead")

    print(df.head())


# ==========================================================
# Weather API
# ==========================================================

def test_weather(
    ingestion: RealtimeIngestion,
):

    section("WEATHER API")

    station = ingestion.station_master.iloc[0]

    response = ingestion.fetcher.fetch_weather(

        station_id=station["station_id"],

        latitude=float(station["latitude"]),

        longitude=float(station["longitude"]),

    )

    print("Success :", response.success)

    if not response.success:

        print(response.error)

        return

    payload = response.payload

    print("Latitude :", payload.get("latitude"))

    print("Longitude:", payload.get("longitude"))

    print("Timezone :", payload.get("timezone"))

    print("Current Keys")

    print(list(payload["current"].keys()))

    print()

    print("Hourly Keys")

    print(list(payload["hourly"].keys()))

    print()

    print(
        "Forecast Hours :",
        len(payload["hourly"]["time"]),
    )


# ==========================================================
# AQI API
# ==========================================================

def test_air_quality(
    ingestion: RealtimeIngestion,
):

    section("AQI API")

    station = ingestion.station_master.iloc[0]

    response = ingestion.fetcher.fetch_air_quality(

        station_id=station["station_id"],

        latitude=float(station["latitude"]),

        longitude=float(station["longitude"]),

    )

    print("Success :", response.success)

    if not response.success:

        print(response.error)

        return

    payload = response.payload

    print("Latitude :", payload.get("latitude"))

    print("Longitude:", payload.get("longitude"))

    print("Timezone :", payload.get("timezone"))

    print("Current Keys")

    print(list(payload["current"].keys()))

    print()

    print("Hourly Keys")

    print(list(payload["hourly"].keys()))

    print()

    print(
        "Forecast Hours :",
        len(payload["hourly"]["time"]),
    )


# ==========================================================
# Single Station
# ==========================================================

def test_single_station(
    ingestion: RealtimeIngestion,
):

    section("SINGLE STATION INGESTION")

    station = ingestion.station_master.iloc[0]

    datasets = ingestion.fetch_station(
        station
    )

    dataframe_summary(
        "Current Weather",
        datasets.current_weather,
    )

    dataframe_summary(
        "Forecast Weather",
        datasets.forecast_weather,
    )

    dataframe_summary(
        "Current AQI",
        datasets.current_air_quality,
    )

    dataframe_summary(
        "Forecast AQI",
        datasets.forecast_air_quality,
    )


# ==========================================================
# Full Ingestion
# ==========================================================

def test_full_ingestion(
    ingestion: RealtimeIngestion,
):

    section("FULL INGESTION")

    datasets = ingestion.fetch_all()

    dataframe_summary(
        "Current Weather",
        datasets.current_weather,
    )

    dataframe_summary(
        "Forecast Weather",
        datasets.forecast_weather,
    )

    dataframe_summary(
        "Current AQI",
        datasets.current_air_quality,
    )

    dataframe_summary(
        "Forecast AQI",
        datasets.forecast_air_quality,
    )

    print()

    print("Fetched At")

    print(datasets.fetched_at)


# ==========================================================
# Main
# ==========================================================

def main():

    ingestion = RealtimeIngestion()

    try:

        test_weather(
            ingestion
        )

        test_air_quality(
            ingestion
        )

        test_single_station(
            ingestion
        )

        test_full_ingestion(
            ingestion
        )

    finally:

        ingestion.close()

    divider()

    print("Realtime pipeline test completed.")

    divider()


if __name__ == "__main__":

    main()