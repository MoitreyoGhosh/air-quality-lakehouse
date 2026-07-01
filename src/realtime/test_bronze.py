"""
test_bronze.py
=====================================

Realtime Bronze Test

Tests
-----
✓ Realtime Ingestion
✓ Bronze Write
✓ DuckDB Registration
✓ Parquet Save
✓ Schema Mapping
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.realtime.ingestion import RealtimeIngestion
from src.realtime.bronze import RealtimeBronze


# ==========================================================
# Helpers
# ==========================================================

BRONZE_DIR = (
    Path("data")
    / "near-real-time"
    / "bronze"
)


def divider():

    print("=" * 80)


def summary(
    name: str,
    df: pd.DataFrame,
):

    print(f"\n{name}")

    print("-" * 80)

    print(f"Rows    : {len(df)}")

    print(f"Columns : {len(df.columns)}")

    if df.empty:

        print("Dataset is empty.")

        return

    print()

    print(df.head())

    print()

    print("Columns")

    print(list(df.columns))


# ==========================================================
# Main
# ==========================================================

def main():

    divider()

    print("REALTIME BRONZE TEST")

    divider()

    ingestion = RealtimeIngestion()

    bronze = RealtimeBronze()

    try:

        # --------------------------------------------------
        # Fetch
        # --------------------------------------------------

        print("\nFetching realtime datasets...")

        datasets = ingestion.fetch_all()

        # --------------------------------------------------
        # Bronze
        # --------------------------------------------------

        print("\nWriting Bronze datasets...")

        bronze_data = bronze.write(
            datasets
        )

        divider()

        print("RETURNED DATASETS")

        divider()

        summary(
            "Current Weather",
            bronze_data.current_weather,
        )

        summary(
            "Forecast Weather",
            bronze_data.forecast_weather,
        )

        summary(
            "Current AQI",
            bronze_data.current_air_quality,
        )

        summary(
            "Forecast AQI",
            bronze_data.forecast_air_quality,
        )

        # --------------------------------------------------
        # DuckDB
        # --------------------------------------------------

        divider()

        print("DUCKDB TABLES")

        divider()

        for table in [

            "realtime_current_weather",

            "realtime_forecast_weather",

            "realtime_current_air_quality",

            "realtime_forecast_air_quality",

        ]:

            df = bronze.read(
                table
            )

            print(
                f"{table:35s} {len(df):8d} rows"
            )

        # --------------------------------------------------
        # Parquet
        # --------------------------------------------------

        divider()

        print("PARQUET FILES")

        divider()

        for file in sorted(

            BRONZE_DIR.glob(
                "*.parquet"
            )

        ):

            df = pd.read_parquet(
                file
            )

            print(

                f"{file.name:40s}"

                f"{len(df):8d} rows"

            )

        divider()

        print("REALTIME BRONZE TEST PASSED")

        divider()

    finally:

        ingestion.close()


if __name__ == "__main__":

    main()