"""
bronze.py
=====================================

Near Real-Time Bronze Layer

Responsibilities
----------------
✓ Execute realtime ingestion
✓ Normalize schema
✓ Resolve aliases
✓ Persist canonical Bronze datasets
✓ Register Bronze tables
✓ Store schema mapping reports
✓ Register metadata

Outputs
-------
data/near-real-time/bronze/

    realtime_current_weather.parquet
    realtime_forecast_weather.parquet
    realtime_current_air_quality.parquet
    realtime_forecast_air_quality.parquet

reports/near-real-time/schema/

metadata/

DuckDB Bronze
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.database.connection import database
from src.database.utils import DatabaseUtils

from src.lakehouse.metadata import metadata

from src.schema.mapper import mapper

from src.realtime.ingestion import (
    RealtimeDatasets
)


# ==========================================================
# Directories
# ==========================================================

BRONZE_DIRECTORY = (
    Path("data")
    / "near-real-time"
    / "bronze"
)

REPORT_DIRECTORY = (
    Path("reports")
    / "near-real-time"
    / "schema"
)

BRONZE_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

REPORT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================================
# Bronze Layer
# ==========================================================

class RealtimeBronze:
    """
    Near Real-Time Bronze Layer.
    """

    def __init__(self):

        self.conn = database.connection

        metadata.initialize()

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def table_name(
        name: str,
    ) -> str:
        """
        Safe DuckDB table name.
        """

        return (
            name.lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

    # ======================================================
    # Schema Mapping
    # ======================================================

    @staticmethod
    def canonicalize(
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Convert dataframe to canonical schema.
        """

        canonical_df, report = mapper.map(df)

        report_df = mapper.report(
            report
        )

        return (
            canonical_df,
            report_df,
        )
    
    # ======================================================
    # Save Dataset
    # ======================================================

    def write_dataset(
        self,
        dataset_name: str,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize and persist one realtime dataset.
        """

        if df.empty:

            print(
                f"Skipping {dataset_name} (empty dataset)."
            )

            return pd.DataFrame()

        # --------------------------------------------------
        # Canonical Schema
        # --------------------------------------------------

        canonical_df, mapping_report = (
            self.canonicalize(df)
        )

        # --------------------------------------------------
        # Lineage
        # --------------------------------------------------

        canonical_df = canonical_df.copy()

        canonical_df["source"] = "OPEN-METEO"

        canonical_df["source_dataset"] = (
            dataset_name
        )

        canonical_df["ingested_at"] = (
            pd.Timestamp.now()
        )

        # --------------------------------------------------
        # Save Mapping Report
        # --------------------------------------------------

        mapping_report.to_csv(

            REPORT_DIRECTORY
            / f"{dataset_name}_mapping.csv",

            index=False,

        )

        # --------------------------------------------------
        # Save Bronze Parquet
        # --------------------------------------------------

        parquet_path = (

            BRONZE_DIRECTORY

            / f"{dataset_name}.parquet"

        )

        canonical_df.to_parquet(

            parquet_path,

            index=False,

        )

        # --------------------------------------------------
        # Register DuckDB
        # --------------------------------------------------

        DatabaseUtils.register(

            "bronze_df",

            canonical_df,

        )

        table = self.table_name(
            dataset_name
        )

        self.conn.execute(
            f"""
            CREATE OR REPLACE TABLE
            bronze.{table}
            AS
            SELECT *
            FROM bronze_df
            """
        )

        DatabaseUtils.unregister(
            "bronze_df"
        )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata.register_dataset(

            dataset_name=dataset_name,

            source="OPEN-METEO",

            layer="bronze",

            rows=len(canonical_df),

            columns=len(canonical_df.columns),

        )

        metadata.log_ingestion(

            dataset_name=dataset_name,

            source="OPEN-METEO",

            layer="bronze",

            status="SUCCESS",

            rows=len(canonical_df),

        )

        print(
            f"Saved {dataset_name}"
        )

        return canonical_df

    # ======================================================
    # Batch Write
    # ======================================================

    def write(
        self,
        datasets: RealtimeDatasets,
    ) -> RealtimeDatasets:
        """
        Normalize, persist and return all realtime datasets.
        """

        current_weather = self.write_dataset(

            "realtime_current_weather",

            datasets.current_weather,

        )

        forecast_weather = self.write_dataset(

            "realtime_forecast_weather",

            datasets.forecast_weather,

        )

        current_air_quality = self.write_dataset(

            "realtime_current_air_quality",

            datasets.current_air_quality,

        )

        forecast_air_quality = self.write_dataset(

            "realtime_forecast_air_quality",

            datasets.forecast_air_quality,

        )

        print()

        print("=" * 80)

        print("REALTIME BRONZE COMPLETE")

        print("=" * 80)

        print()

        return RealtimeDatasets(

            current_weather=current_weather,

            forecast_weather=forecast_weather,

            current_air_quality=current_air_quality,

            forecast_air_quality=forecast_air_quality,

            fetched_at=datasets.fetched_at,

        )
    

    # ======================================================
    # Read Dataset
    # ======================================================

    def read(
        self,
        dataset_name: str,
    ) -> pd.DataFrame:
        """
        Read a Bronze dataset from DuckDB.
        """

        table = self.table_name(
            dataset_name
        )

        return DatabaseUtils.query(
            f"""
            SELECT *
            FROM bronze.{table}
            """
        )

    # ======================================================
    # Read All
    # ======================================================

    def read_all(
        self,
    ) -> RealtimeDatasets:
        """
        Read all Bronze realtime datasets.
        """

        return RealtimeDatasets(

            current_weather=self.read(
                "realtime_current_weather"
            ),

            forecast_weather=self.read(
                "realtime_forecast_weather"
            ),

            current_air_quality=self.read(
                "realtime_current_air_quality"
            ),

            forecast_air_quality=self.read(
                "realtime_forecast_air_quality"
            ),

            fetched_at=pd.Timestamp.now(),

        )

    # ======================================================
    # Summary
    # ======================================================

    @staticmethod
    def summary() -> pd.DataFrame:
        """
        Return Bronze dataset registry.
        """

        return metadata.dataset_registry()


# ==========================================================
# Singleton
# ==========================================================

realtime_bronze = RealtimeBronze()