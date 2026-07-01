"""
silver.py
==============================================

Environmental Intelligence Lakehouse

Silver Layer

Responsibilities
----------------
1. Build WBPCB Master
2. Build Weather Master
3. Build Environment Master
4. Generate Cleaning Reports
5. Save DuckDB Tables
6. Export Parquet Files
7. Validate Curated Datasets

Silver Layer becomes the trusted source for:

• Gold Layer
• Analytics
• Forecasting
• Machine Learning
• Dashboarding

Author:
MG
"""

from __future__ import annotations

from pathlib import Path
import re
import pandas as pd

from src.database.connection import database
from src.database.utils import DatabaseUtils


class SilverLayer:
    """
    Curated Lakehouse Silver Layer.

    Bronze
        ↓
    Cleaning
        ↓
    Master Dataset Generation
        ↓
    DuckDB Tables
        +
    Parquet Files
    """

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(self):

        self.connection = database.connection

        self.project_root = Path.cwd()

        self.silver_directory = (
            self.project_root
            / "data"
            / "silver"
        )

        self.silver_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.metadata_directory = (
            self.project_root
            / "data"
            / "metadata"
        )

        self.metadata_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ==========================================================
    # Bronze Helpers
    # ==========================================================

    @staticmethod
    def bronze_tables() -> list[str]:

        return DatabaseUtils.list_tables(
            "bronze"
        )

    @staticmethod
    def read(table: str) -> pd.DataFrame:

        return DatabaseUtils.query(
            f"""
            SELECT *
            FROM bronze.{table}
            """
        )

    # ==========================================================
    # Metadata
    # ==========================================================

    @staticmethod
    def station_metadata() -> pd.DataFrame:

        return DatabaseUtils.query(
            """
            SELECT *
            FROM metadata.station_master
            """
        )

    # ==========================================================
    # Generic Save
    # ==========================================================

    def save_duckdb(
        self,
        table: str,
        df: pd.DataFrame,
    ) -> None:

        DatabaseUtils.register(
            "_silver_temp",
            df,
        )

        self.connection.execute(
            f"""
            CREATE OR REPLACE TABLE
            silver.{table}
            AS
            SELECT *
            FROM _silver_temp
            """
        )

        DatabaseUtils.unregister(
            "_silver_temp"
        )

    def save_parquet(
        self,
        table: str,
        df: pd.DataFrame,
    ) -> None:

        path = (
            self.silver_directory
            / f"{table}.parquet"
        )

        df.to_parquet(
            path,
            index=False,
        )

        assert path.exists(), (
            f"Parquet export failed: {path}"
        )

    def save_master(
        self,
        table: str,
        df: pd.DataFrame,
    ) -> None:

        self.save_duckdb(
            table,
            df,
        )

        self.save_parquet(
            table,
            df,
        )

        print(
            f"✓ Saved silver.{table}"
        )

        print(
            f"✓ Saved {table}.parquet"
        )

    # ==========================================================
    # Reports
    # ==========================================================

    def save_report(
        self,
        table: str,
        report: pd.DataFrame,
    ) -> None:

        DatabaseUtils.register(
            "_report",
            report,
        )

        self.connection.execute(
            f"""
            CREATE OR REPLACE TABLE
            metadata.{table}
            AS
            SELECT *
            FROM _report
            """
        )

        DatabaseUtils.unregister(
            "_report"
        )

    # ==========================================================
    # Utility
    # ==========================================================

    @staticmethod
    def normalize_station(value: str) -> str:

        if pd.isna(value):
            return ""

        value = (
            str(value)
            .lower()
            .replace("&", "and")
            .replace("-", " ")
            .replace("_", " ")
            .replace(".", "")
            .replace(",", "")
            .replace("'", "")
            .replace("(", "")
            .replace(")", "")
        )   

        value = re.sub(r"\s+", " ", value)

        return value.strip()

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

    # ==========================================================
    # Logging
    # ==========================================================

    @staticmethod
    def banner(title: str):

        print("\n")

        print("=" * 90)

        print(title)

        print("=" * 90)

    @staticmethod
    def divider():

        print("-" * 90)

    # ==========================================================
    # Run Complete Silver Layer
    # ==========================================================
    def run(self):
        wbpcb_master, wbpcb_report = self.build_wbpcb_master()
        weather_master, weather_report = self.build_weather_master()
        environment_master = self.build_environment_master()
        return {
            "wbpcb_master": wbpcb_master,
            "weather_master": weather_master,
            "environment_master": environment_master,
            "wbpcb_report": wbpcb_report,
            "weather_report": weather_report,
        }
    
    # ==========================================================
    # WBPCB MASTER
    # ==========================================================

    def build_wbpcb_master(
        self,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:

        self.banner(
            "BUILDING WBPCB MASTER"
        )

        metadata = self.station_metadata().copy()

        metadata["_station_key"] = (
            metadata["wbpcb_station"]
            .apply(self.normalize_station)
        )

        metadata = metadata[
            [
                "_station_key",
                "station_id",
                "station_name",
                "district",
                "latitude",
                "longitude",
            ]
        ].drop_duplicates("_station_key") 

        bronze_tables = [

            table

            for table in self.bronze_tables()

            if not table.startswith(
                "open_meteo"
            )

        ]

        bronze_tables = sorted(
            bronze_tables
        )

        master = []

        reports = []

        # ======================================================
        # Process every Bronze dataset
        # ======================================================

        for table in bronze_tables:

            print(
                f"Loading : {table}"
            )

            df = self.read(table)

            required_columns = {
                "station",
                "date",
                "hour",
                "aqi",
            }

            missing = required_columns - set(df.columns)

            if missing:
                raise ValueError(
                    f"{table} is missing required columns: {sorted(missing)}"
                )

            original_rows = len(df)

            original_columns = len(
                df.columns
            )

            # --------------------------------------------
            # Remove empty columns
            # --------------------------------------------

            df = df.dropna(
                axis=1,
                how="all",
            )

            empty_removed = (

                original_columns

                - len(df.columns)

            )

            # --------------------------------------------
            # Remove duplicate rows
            # --------------------------------------------

            df = df.drop_duplicates()

            duplicates_removed = (

                original_rows

                - len(df)

            )

            # ======================================================
            # Datetime
            # ======================================================

            # Clean hour column
            df["hour"] = (
                df["hour"]
                .astype(str)
                .str.strip()
            )

            # Convert 0–23 into HH:00:00
            mask = df["hour"].str.fullmatch(r"\d{1,2}")

            df.loc[mask, "hour"] = (
                df.loc[mask, "hour"]
                .str.zfill(2)
                + ":00:00"
            )

            # Convert HH:MM into HH:MM:00
            mask = df["hour"].str.fullmatch(
                r"\d{1,2}:\d{2}"
            )

            df.loc[mask, "hour"] = (
                df.loc[mask, "hour"]
                + ":00"
            )

            datetime_string = (
                df["date"].astype(str)
                .str.strip()
                + " "
                + df["hour"]
            )

            df["datetime"] = pd.to_datetime(
                datetime_string,
                errors="coerce",
            )

            invalid_datetime = int(
                df["datetime"].isna().sum()
            )

            if invalid_datetime:
            
                print(f"{table}: {invalid_datetime} invalid timestamps detected.")

                invalid_rows = df.loc[
                    df["datetime"].isna(),
                    ["date", "hour"]
                ].copy()

                if not invalid_rows.empty:
                
                    invalid_rows.to_csv(
                        self.metadata_directory
                        / f"{table}_invalid_datetime.csv",
                        index=False,
                    )

                    print(
                        f"Saved {len(invalid_rows)} invalid timestamps "
                        f"to {table}_invalid_datetime.csv"
                    )

            df = df.dropna(
                subset=["datetime"]
            )

            # --------------------------------------------
            # Station Mapping
            # --------------------------------------------

            df["_station_key"] = (

                df["station"]

                .apply(
                    self.normalize_station
                )

            )
    
            df = df.merge(
                metadata,
                on="_station_key",
                how="left",
            )

            # --------------------------------------------
            # Resolve duplicate metadata columns
            # --------------------------------------------
            
            for column in [
                "district",
                "latitude",
                "longitude",
            ]:
            
                left = f"{column}_x"
                right = f"{column}_y"
            
                if left in df.columns and right in df.columns:
                
                    same = (
                        df[left]
                        .fillna("")
                        .equals(
                            df[right]
                            .fillna("")
                        )
                    )
            
                    if same:
                    
                        df = df.drop(
                            columns=[right]
                        )
            
                        df = df.rename(
                            columns={
                                left: column
                            }
                        )
            
                    else:
                    
                        print(
                            f"Warning: {table} -> "
                            f"'{column}' differs between WBPCB and metadata."
                        )
            
                        # Metadata is the authoritative source
                        df = df.drop(
                            columns=[left]
                        )
            
                        df = df.rename(
                            columns={
                                right: column
                            }
                        )

            unmapped = int(
                df["station_id"]
                .isna()
                .sum()
            )

            if unmapped > 0:

                raise ValueError(
                    f"{table}: {unmapped} stations could not be mapped."
                )
            
            # --------------------------------------------
            # Cleanup
            # --------------------------------------------

            df = df.drop(

                columns=[
                    "_station_key",
                    "date",
                    "hour",
                    "station",
                ],
                errors="ignore",
            )

            master.append(df)

            reports.append({
                "dataset": table,
                "source": "WBPCB",
                "original_rows": original_rows,
                "final_rows": len(df),
                "duplicates_removed": duplicates_removed,
                "empty_columns_removed": empty_removed,
                "invalid_datetime": invalid_datetime,
                "unmapped_stations": unmapped,
            })

        # ======================================================
        # Merge all datasets
        # ======================================================

        wbpcb_master = pd.concat(
            master,
            ignore_index=True,
        )

        before = len(wbpcb_master)

        wbpcb_master = wbpcb_master.drop_duplicates(
            subset=[
                "station_id",
                "datetime",
            ]
        )

        print(
            "Duplicates removed after merge:",
            before - len(wbpcb_master),
        )

        # ======================================================
        # Optimize
        # ======================================================

        wbpcb_master = self.optimize_dataframe(
            wbpcb_master
        )

        wbpcb_master = (

            wbpcb_master

            .sort_values(

                [

                    "station_id",

                    "datetime",

                ]

            )

            .reset_index(

                drop=True

            )

        )

        # ======================================================
        # Validation
        # ======================================================

        self.divider()

        print(
            "Rows :",
            len(
                wbpcb_master
            ),
        )

        print(
            "Stations :",
            wbpcb_master[
                "station_id"
            ].nunique(),
        )

        duplicates = self.validate_duplicates(

            wbpcb_master,

            [

                "station_id",

                "datetime",

            ],

        )

        print(

            "Duplicate Station-Time :",

            duplicates,

        )

        print()

        print(
            "Missing Values"
        )

        print(

            self.missing_summary(

                wbpcb_master

            )

        )

        # ======================================================
        # Save
        # ======================================================

        self.save_master(

            "wbpcb_master",

            wbpcb_master,

        )

        report_df = pd.DataFrame(
            reports
        )

        self.save_report(

            "wbpcb_cleaning_report",

            report_df,

        )

        print()

        print(
            "WBPCB MASTER COMPLETE"
        )

        return (

            wbpcb_master,

            report_df,

        )
    
    # ==========================================================
    # WEATHER MASTER
    # ==========================================================

    def build_weather_master(
        self,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:

        self.banner(
            "BUILDING WEATHER MASTER"
        )

        # ======================================================
        # Load Station Metadata
        # ======================================================

        metadata = self.station_metadata().copy()

        metadata = metadata[
            [
                "station_id",
                "station_name",
                "district",
                "latitude",
                "longitude",
                "openmeteo_dataset",
            ]
        ].drop_duplicates(
            subset=["openmeteo_dataset"]
        )

        # ======================================================
        # Discover Bronze Weather Tables
        # ======================================================

        weather_tables = sorted(
            [
                table
                for table in self.bronze_tables()
                if table.startswith("open_meteo")
            ]
        )

        if not weather_tables:

            raise RuntimeError(
                "No Open-Meteo Bronze tables found."
            )

        weather_master = []

        report = []

        # ======================================================
        # Process Every Weather Dataset
        # ======================================================

        for table in weather_tables:

            self.divider()

            print(
                f"Processing : {table}"
            )

            df = self.read(table)

            original_rows = len(df)

            original_columns = len(df.columns)

            # ==================================================
            # Validate Schema
            # ==================================================

            required_columns = {
             "time",
             "temperature",
             "humidity",
             "dew_point",
             "precipitation",
             "pressure",
             "cloud_cover",
             "wind_speed",
             "wind_direction",
             "wind_gust",
            }

            missing = (
                required_columns
                - set(df.columns)
            )

            if missing:

                raise ValueError(

                    f"{table} missing columns : "

                    f"{sorted(missing)}"

                )

            # ==================================================
            # Remove Empty Columns
            # ==================================================

            df = df.dropna(
                axis=1,
                how="all",
            )

            empty_columns_removed = (

                original_columns

                - len(df.columns)

            )

            # ==================================================
            # Remove Duplicate Rows
            # ==================================================

            before_duplicates = len(df)

            df = df.drop_duplicates()

            duplicates_removed = (

                before_duplicates

                - len(df)

            )

            # ==================================================
            # Generate Datetime
            # ==================================================

            df["datetime"] = pd.to_datetime(
                df["time"],
                errors="coerce",
            )

            before_datetime = len(df)

            df = df.dropna(
                subset=[
                    "datetime"
                ]
            )

            invalid_datetime = (

                before_datetime

                - len(df)

            )

            # ==================================================
            # Remove Original Time Column
            # ==================================================

            df = df.drop(
                columns=[
                    "time",
                ],
                errors="ignore",
            )

            # ==================================================
            # Attach Metadata
            # ==================================================

            dataset_name = (
            df["source_dataset"]
            .iloc[0]
            .strip()
             )

            lookup = metadata.loc[
                metadata["openmeteo_dataset"] == dataset_name
            ]

            if lookup.empty:
                raise ValueError(
                    f"No station metadata found for '{table}'."
                )

            station = lookup.iloc[0]

            df["station_id"] = (
                station["station_id"]
            )

            df["station_name"] = (
                station["station_name"]
            )

            df["district"] = (
                station["district"]
            )

            df["latitude"] = (
                station["latitude"]
            )

            df["longitude"] = (
                station["longitude"]
            )

            # ==================================================
            # Canonical Column Order
            # ==================================================

            df = df[
                [
                    "station_id",
                    "station_name",
                    "district",
                    "latitude",
                    "longitude",
                    "datetime",
                    "temperature",
                    "humidity",
                    "dew_point",
                    "precipitation",
                    "pressure",
                    "cloud_cover",
                    "wind_speed",
                    "wind_direction",
                    "wind_gust",
                ]
            ]

            weather_master.append(df)

            report.append(
                {
                    "dataset": dataset_name,
                    "station_id": station["station_id"],
                    "original_rows": original_rows,
                    "final_rows": len(df),
                    "duplicates_removed": duplicates_removed,
                    "empty_columns_removed": empty_columns_removed,
                    "invalid_datetime": invalid_datetime,
                }
            )

        # ======================================================
        # Concatenate All Stations
        # ======================================================

        self.divider()

        print("Concatenating Weather Datasets...")

        weather_master = pd.concat(
            weather_master,
            ignore_index=True,
        )

        # ======================================================
        # Remove Cross-Dataset Duplicates
        # ======================================================

        before = len(weather_master)

        weather_master = weather_master.drop_duplicates(
            subset=[
                "station_id",
                "datetime",
            ]
        )

        print(
            "Duplicates removed after merge :",
            before - len(weather_master),
        )

        # ======================================================
        # Sort Dataset
        # ======================================================

        weather_master = (
            weather_master
            .sort_values(
                [
                    "station_id",
                    "datetime",
                ]
            )
            .reset_index(
                drop=True,
            )
        )

        # ======================================================
        # Optimize Data Types
        # ======================================================

        weather_master = self.optimize_dataframe(
            weather_master
        )

        # ======================================================
        # Validation
        # ======================================================

        self.banner(
            "WEATHER MASTER VALIDATION"
        )

        print(
            f"Rows                : {len(weather_master)}"
        )

        print(
            f"Stations            : "
            f"{weather_master['station_id'].nunique()}"
        )

        print(
            f"Columns             : "
            f"{len(weather_master.columns)}"
        )

        print(
            f"Date Start          : "
            f"{weather_master['datetime'].min()}"
        )

        print(
            f"Date End            : "
            f"{weather_master['datetime'].max()}"
        )

        duplicates = self.validate_duplicates(
            weather_master,
            [
                "station_id",
                "datetime",
            ],
        )

        print(
            f"Duplicate Records   : {duplicates}"
        )

        # ======================================================
        # Missing Values
        # ======================================================

        print("\nMissing Values")

        print(
            self.missing_summary(
                weather_master
            )
        )

        # ======================================================
        # Weather Feature Coverage
        # ======================================================

        weather_features = [
            "temperature",
            "humidity",
            "dew_point",
            "precipitation",
            "pressure",
            "cloud_cover",
            "wind_speed",
            "wind_direction",
            "wind_gust",
        ]

        print("\nWeather Feature Coverage")

        for feature in weather_features:

            if feature in weather_master.columns:

                missing = weather_master[
                    feature
                ].isna().sum()

                coverage = (
                    100
                    * (
                        1
                        - weather_master[
                            feature
                        ].isna().mean()
                    )
                )

                print(
                    f"{feature:20s}"
                    f" Missing: {missing:8d}"
                    f" Coverage: {coverage:6.2f}%"
                )

        # ======================================================
        # Save Weather Master
        # ======================================================

        self.save_master(
            "weather_master",
            weather_master,
        )

        # ======================================================
        # Save Cleaning Report
        # ======================================================

        report_df = pd.DataFrame(report)

        self.save_report(
            "weather_cleaning_report",
            report_df,
        )

        print()

        print(
            "✓ Weather Master Created Successfully"
        )

        return (
            weather_master,
            report_df,
        )

    # ==========================================================
    # ENVIRONMENT MASTER
    # ==========================================================

    def build_environment_master(
        self,
    ) -> pd.DataFrame:

        self.banner(
            "BUILDING ENVIRONMENT MASTER"
        )

        # ======================================================
        # Read Masters directly
        # ======================================================

        wbpcb = DatabaseUtils.query(
            """
            SELECT *
            FROM silver.wbpcb_master
            """
        )

        weather = DatabaseUtils.query(
            """
            SELECT *
            FROM silver.weather_master
            """
        )

        # ======================================================
        # Validate Required Columns
        # ======================================================

        wbpcb_required = {
            "station_id",
            "datetime",
            "aqi",
            "pm25",
            "pm10",
        }

        weather_required = {
            "station_id",
            "datetime",
            "temperature",
            "humidity",
            "dew_point",
            "precipitation",
            "pressure",
            "cloud_cover",
            "wind_speed",
            "wind_direction",
            "wind_gust",
        }

        missing = wbpcb_required - set(wbpcb.columns)

        if missing:
            raise ValueError(
                f"WBPCB Master missing columns: {sorted(missing)}"
            )

        missing = weather_required - set(weather.columns)

        if missing:
            raise ValueError(
                f"Weather Master missing columns: {sorted(missing)}"
            )

        # ======================================================
        # Ensure Datatypes
        # ======================================================

        wbpcb["station_id"] = (
            wbpcb["station_id"]
            .astype(str)
        )

        weather["station_id"] = (
            weather["station_id"]
            .astype(str)
        )

        wbpcb["datetime"] = pd.to_datetime(
            wbpcb["datetime"]
        )

        weather["datetime"] = pd.to_datetime(
            weather["datetime"]
        )

        # ======================================================
        # Remove duplicated metadata
        # ======================================================

        weather = weather.drop(
            columns=[
                "station_name",
                "district",
                "latitude",
                "longitude",
            ],
            errors="ignore",
        )

        # ======================================================
        # Merge
        # ======================================================

        environment = wbpcb.merge(
            weather,
            how="left",
            on=[
                "station_id",
                "datetime",
            ],
            suffixes=(
                "",
                "_weather",
            ),
            indicator=True
        )

        print("\nMerge Statistics")

        merge_stats = environment["_merge"].value_counts()

        print(merge_stats)
        
        left_only = merge_stats.get("left_only", 0)
        
        if left_only > 0:
            print(
                f"\nWARNING: {left_only} WBPCB records have no matching weather observation."
            )

        environment.drop(
            columns="_merge",
            inplace=True,
        )

        # ======================================================
        # Remove obsolete WBPCB wind variables
        # ======================================================

        environment = environment.drop(
            columns=[
                "wind_direction",
                "wind_speed",
                "wind_speed_min",
                "wind_speed_max",
            ],
            errors="ignore",
        )

        # ======================================================
        # Rename Weather Wind
        # ======================================================

        rename_columns = {

            "wind_direction_weather":
                "wind_direction",

            "wind_speed_weather":
                "wind_speed",

            "wind_gust_weather":
                "wind_gust",

        }

        environment = environment.rename(
            columns=rename_columns
        )


        # ======================================================
        # Weather Feature Coverage
        # ======================================================

        weather_features = [
            "temperature",
            "humidity",
            "dew_point",
            "precipitation",
            "pressure",
            "cloud_cover",
            "wind_speed",
            "wind_direction",
            "wind_gust",
        ]

        print("\nWeather Feature Coverage")

        for feature in weather_features:
        
            if feature in environment.columns:
                
                missing = environment[feature].isna().sum()

                coverage = (
                    100
                    * (
                        1
                        - environment[feature].isna().mean()
                    )
                )

                print(
                    f"{feature:20s}"
                    f" Missing: {missing:8d}"
                    f" Coverage: {coverage:6.2f}%"
                )

        # ======================================================
        # Remove Duplicates
        # ======================================================

        before = len(environment)

        environment = environment.drop_duplicates(
            subset=[
                "station_id",
                "datetime",
            ]
        )
        print(
            "Duplicates removed after merge:",
            before - len(environment),
        )

        # ======================================================
        # Sort
        # ======================================================

        environment = (
            environment
            .sort_values(
                [
                    "station_id",
                    "datetime",
                ]
            )
            .reset_index(
                drop=True
            )
        )

        # ======================================================
        # Optimize
        # ======================================================

        environment = self.optimize_dataframe(
            environment
        )

        # ======================================================
        # Canonical Column Order
        # ======================================================

        columns = [
            "station_id",
            "station_name",
            "district",
            "latitude",
            "longitude",
            "datetime",
            "aqi",
            "pm25",
            "pm10",
            "temperature",
            "humidity",
            "dew_point",
            "precipitation",
            "pressure",
            "cloud_cover",
            "wind_speed",
            "wind_direction",
            "wind_gust",
        ]

        environment = environment[
            [
                c
                for c in columns
                if c in environment.columns
            ]
        ]

        # ======================================================
        # Validation
        # ======================================================
        self.divider()

        print("Rows :", len(environment))
        print("Stations :",environment["station_id"].nunique())

        duplicates = self.validate_duplicates(
            environment,
            [
                "station_id",
                "datetime",
            ],
        )

        print("Duplicate Station-Time :",duplicates)
        print()
        print("Missing Values")
        print(self.missing_summary(environment))


        # ====================================================
        # Validation Summary
        # ====================================================
        print("=" * 80)
        print("ENVIRONMENT MASTER VALIDATION")
        print("=" * 80)

        print(f"Rows: {len(environment)}")
        print(f"Columns: {len(environment.columns)}")
        print(f"Stations: {environment['station_id'].nunique()}")
        print(f"Date Start: {environment['datetime'].min()}")
        print(f"Date End: {environment['datetime'].max()}")

        dup = environment.duplicated(
            subset=["station_id", "datetime"]
        ).sum()

        print(f"Duplicate Station-Time: {dup}")
        print()

        for col in environment.columns:
            pct = environment[col].isna().mean() * 100
            print(
                f"{col:25s}"
                f"{environment[col].isna().sum():8d}"
                f"{pct:8.2f}%"
            )

        assert (
            self.validate_duplicates(
                environment,
                ["station_id","datetime"]
            ) == 0
        )

        assert (
            environment["datetime"].notna().all()
        )

        assert (
            environment["station_id"].notna().all()
        )    

        # ======================================================
        # Save
        # ======================================================

        self.save_master(
            "environment_master",
            environment,
        )

        print()

        print("ENVIRONMENT MASTER COMPLETE")
        return environment
