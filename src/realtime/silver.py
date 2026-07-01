"""
silver.py
=====================================

Near Real-Time Silver Layer

Responsibilities
----------------
✓ Read Bronze datasets
✓ Build Current Master
✓ Build Forecast Master
✓ Build Realtime Master
✓ Remove duplicates
✓ Optimize datatypes
✓ Validate datasets
✓ Save realtime_master.parquet

Output
------
data/near-real-time/silver/

    realtime_master.parquet
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


from src.realtime.bronze import RealtimeBronze
from src.realtime.ingestion import RealtimeDatasets


# ==========================================================
# Directories
# ==========================================================

SILVER_DIRECTORY = (
    Path("data")
    / "near-real-time"
    / "silver"
)

SILVER_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

# ==========================================================
# Silver Layer
# ==========================================================

class RealtimeSilver:
    """
    Near Real-Time Silver Layer.
    """

    def __init__(self):

        super().__init__()

        self.bronze = RealtimeBronze()

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def divider():

        print("=" * 80)

    @staticmethod
    def banner(
        title: str,
    ):

        print()

        print("=" * 80)

        print(title)

        print("=" * 80)

    # ==========================================================
    # Utilities
    # ==========================================================

    @staticmethod
    def validate_duplicates(
        df: pd.DataFrame,
        columns: list[str],
    ) -> int:

        return int(
            df.duplicated(
                subset=columns
            ).sum()
        )

    @staticmethod
    def missing_summary(
        df: pd.DataFrame,
    ) -> pd.Series:

        return (
            df
            .isna()
            .sum()
            .sort_values(
                ascending=False
            )
        )

    @staticmethod
    def optimize_dataframe(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in df.columns:

            if pd.api.types.is_float_dtype(
                df[column]
            ):

                df[column] = pd.to_numeric(
                    df[column],
                    downcast="float",
                )

            elif pd.api.types.is_integer_dtype(
                df[column]
            ):

                df[column] = pd.to_numeric(
                    df[column],
                    downcast="integer",
                )

        return df

    # ======================================================
    # Read Bronze
    # ======================================================

    def bronze_data(
        self,
    ) -> RealtimeDatasets:
        """
        Load Bronze datasets.
        """

        return self.bronze.read_all()

    # ======================================================
    # Save
    # ======================================================

    @staticmethod
    def save(
        df: pd.DataFrame,
    ) -> None:
        """
        Save realtime master parquet.
        """

        path = (
            SILVER_DIRECTORY
            / "realtime_master.parquet"
        )

        df.to_parquet(
            path,
            index=False,
        )

        print(
            "✓ Saved realtime_master.parquet"
        )

    # ======================================================
    # Optimize
    # ======================================================
    
    def optimize(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        return self.optimize_dataframe(df)
    
    # ======================================================
    # Current Master
    # ======================================================

    def build_current_master(
        self,
        datasets: RealtimeDatasets,
    ) -> pd.DataFrame:
        """
        Merge current weather and current AQI.
        """

        self.banner(
            "BUILDING CURRENT MASTER"
        )

        current = datasets.current_weather.merge(

            datasets.current_air_quality,

            on=[
                "station_id",
                "time",
            ],

            how="left",

            suffixes=(
                "",
                "_aqi",
            ),

        )

        # ----------------------------------------------
        # Remove duplicate metadata
        # ----------------------------------------------

        duplicate_columns = [

            column

            for column in current.columns

            if column.endswith("_aqi")

        ]

        current = current.drop(
            columns=duplicate_columns,
            errors="ignore",
        )

        current["record_type"] = "current"

        print(
            "Rows :",
            len(current),
        )

        return current

    # ======================================================
    # Forecast Master
    # ======================================================

    def build_forecast_master(
        self,
        datasets: RealtimeDatasets,
    ) -> pd.DataFrame:
        """
        Merge forecast weather and AQI.
        """

        self.banner(
            "BUILDING FORECAST MASTER"
        )

        forecast = datasets.forecast_weather.merge(
            datasets.forecast_air_quality,
            on=[
                "station_id",
                "time",
            ],
            how="left",
            suffixes=(
                "",
                "_aqi",
            ),

        )

        duplicate_columns = [
            column
            for column in forecast.columns
            if column.endswith("_aqi")
        ]

        forecast = forecast.drop(
            columns=duplicate_columns,
            errors="ignore",

        )

        forecast["record_type"] = (
            "forecast"
        )

        print(
            "Rows :",
            len(forecast),
        )

        return forecast

    # ======================================================
    # Realtime Master
    # ======================================================

    def build_realtime_master(
        self,
        datasets: RealtimeDatasets,
    ) -> pd.DataFrame:
        """
        Build unified realtime dataset.
        """

        self.banner(
            "BUILDING REALTIME MASTER"
        )

        current = self.build_current_master(
            datasets
        )

        forecast = self.build_forecast_master(
            datasets
        )

        master = pd.concat(
            [
                current,
                forecast,
            ],
            ignore_index=True,
        )

        # ----------------------------------------------
        # Datetime
        # ----------------------------------------------

        master = master.rename(
            columns={
                "time": "datetime",
            }
        )

        master["datetime"] = pd.to_datetime(
            master["datetime"],
            errors="coerce",
        )

        # ----------------------------------------------
        # Cleanup
        # ----------------------------------------------

        master = master.drop(
            columns=[
                "interval",
            ],
            errors="ignore",
        )

        before = len(master)

        master = master.drop_duplicates(
            subset=[
                "station_id",
                "datetime",
                "record_type",
            ]
        )

        print(
            "Duplicates removed :",
            before - len(master),
        )

        master = (
            master
            .sort_values(
                [
                    "station_id",
                    "datetime"
                ]
            )
            .reset_index(
                drop=True
            )
        )

        master = self.optimize(
            master
        )

        return master
    

    # ======================================================
    # Validation
    # ======================================================

    def validate(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Validate realtime master dataset.
        """

        self.banner(
            "REALTIME VALIDATION"
        )

        print(
            "Rows :",
            len(df),
        )

        print(
            "Columns :",
            len(df.columns),
        )

        print(
            "Stations :",
            df["station_id"].nunique(),
        )

        print(
            "Datetime Range :"
        )

        print(
            df["datetime"].min(),
            "->",
            df["datetime"].max(),
        )

        duplicates = self.validate_duplicates(

            df,

            [
                "station_id",
                "datetime",
                "record_type",
            ],

        )

        print()

        print(
            "Duplicate Records :",
            duplicates,
        )

        print()

        print(
            "Missing Values"
        )

        print(
            self.missing_summary(df)
        )

    # ======================================================
    # Pipeline
    # ======================================================

    def run(
        self,
        datasets: RealtimeDatasets | None = None,
    ) -> pd.DataFrame:
        """
        Execute Realtime Silver pipeline.
        """

        self.banner(
            "REALTIME SILVER"
        )

        # --------------------------------------------------
        # Load Bronze
        # --------------------------------------------------

        if datasets is None:
            datasets = self.bronze_data()

        realtime_master = self.build_realtime_master(
            datasets
        )

        self.validate(
            realtime_master
        )

        self.save(
            realtime_master
        )

        self.banner(
            "REALTIME SILVER COMPLETE"
        )

        return realtime_master


# ==========================================================
# Singleton
# ==========================================================

realtime_silver = RealtimeSilver()