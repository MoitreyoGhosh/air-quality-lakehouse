"""
realtime_pipeline.py
=====================================

Near Real-Time Environmental Pipeline

Pipeline
--------
Open-Meteo APIs
        │
        ▼
Realtime Fetcher
        │
        ▼
Realtime Ingestion
        │
        ▼
Realtime Bronze
        │
        ▼
Realtime Silver
        │
        ▼
realtime_master.parquet
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.realtime.ingestion import RealtimeIngestion
from src.realtime.bronze import RealtimeBronze
from src.realtime.silver import RealtimeSilver


class RealtimePipeline:
    """
    Execute the complete Near Real-Time pipeline.
    """

    def __init__(self):

        self.ingestion = RealtimeIngestion()

        self.bronze = RealtimeBronze()

        self.silver = RealtimeSilver()

    @staticmethod
    def divider():

        print("=" * 80)

    @staticmethod
    def banner(title: str):

        print()

        print("=" * 80)

        print(title)

        print("=" * 80)

    def run(self) -> pd.DataFrame:
        """
        Execute the complete realtime ETL pipeline.
        """

        self.banner(
            "NEAR REAL-TIME PIPELINE"
        )

        # ==================================================
        # Step 1 : Fetch API Data
        # ==================================================

        print("\n[1/3] Fetching Open-Meteo Data\n")

        datasets = self.ingestion.fetch_all()

        # ==================================================
        # Step 2 : Bronze Layer
        # ==================================================

        print("\n[2/3] Bronze Layer\n")

        bronze_data = self.bronze.write(
            datasets
        )

        # ==================================================
        # Step 3 : Silver Layer
        # ==================================================

        print("\n[3/3] Silver Layer\n")

        realtime_master = self.silver.run(
            datasets=bronze_data
        )

        # ==================================================
        # Summary
        # ==================================================

        self.banner(
            "PIPELINE SUMMARY"
        )

        print(
            f"Stations        : {realtime_master['station_id'].nunique()}"
        )

        print(
            f"Rows            : {len(realtime_master)}"
        )

        print(
            f"Columns         : {len(realtime_master.columns)}"
        )

        print(
            "Datetime Range  :",
            realtime_master["datetime"].min(),
            "->",
            realtime_master["datetime"].max(),
        )

        print()
        print("Realtime Pipeline Completed Successfully.")
        return realtime_master


# ==========================================================
# Entry Point
# ==========================================================

def main():
    pipeline = RealtimePipeline()
    pipeline.run()


if __name__ == "__main__":
    main()