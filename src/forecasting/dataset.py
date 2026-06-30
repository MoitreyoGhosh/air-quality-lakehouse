"""
dataset.py

Dataset Loader for the Environmental Intelligence Lakehouse.

Responsibilities
----------------
1. Load data from DuckDB
2. Select target variable
3. Prepare ML-ready dataset
4. Basic cleaning
"""

from typing import List, Optional

import pandas as pd

from src.analytics.analytics import AnalyticsEngine


class DatasetLoader:
    """
    Loads environmental datasets from DuckDB.
    """

    def __init__(self):
        self.engine = AnalyticsEngine()

    # =====================================================
    # Load Environmental Master
    # =====================================================

    def load_environmental_master(self) -> pd.DataFrame:
        """
        Load the complete environmental master dataset.
        """

        df = self.engine.environmental_master()

        df["datetime"] = pd.to_datetime(df["datetime"])

        return df

    # =====================================================
    # Prepare Dataset
    # =====================================================

    def prepare_dataset(
        self,
        target: str = "aqi",
        features: Optional[List[str]] = None,
        drop_missing: bool = True
    ) -> pd.DataFrame:
        """
        Prepare a dataset for machine learning.

        Parameters
        ----------
        target : str
            Target variable (aqi, pm25, pm10)

        features : list
            Feature columns to retain.
            If None, sensible defaults are used.

        drop_missing : bool
            Remove rows with missing values.
        """

        df = self.load_environmental_master()

        if features is None:

            features = [

                "datetime",
                "station_id",
                "station_name",

                "temperature",
                "humidity",

                "wind_speed_avg",
                "wind_direction",

                "pm25",
                "pm10",
                "aqi"

            ]

        existing_columns = [
            col for col in features
            if col in df.columns
        ]

        if target not in existing_columns:
            existing_columns.append(target)

        df = df[existing_columns]

        if drop_missing:
            df = df.dropna()

        df = df.sort_values(
            [
                "station_id",
                "datetime"
            ]
        )

        df = df.reset_index(drop=True)

        return df

    # =====================================================
    # Station Dataset
    # =====================================================

    def station_dataset(
        self,
        station_name: str,
        target: str = "aqi"
    ) -> pd.DataFrame:
        """
        Return dataset for one station only.
        """

        df = self.prepare_dataset(target=target)

        df = df[
            df["station_name"] == station_name
        ]

        return df.reset_index(drop=True)

    # =====================================================
    # Date Range
    # =====================================================

    def date_range(
        self,
        start_date: str,
        end_date: str,
        target: str = "aqi"
    ) -> pd.DataFrame:
        """
        Return data within a specified date range.
        """

        df = self.prepare_dataset(target=target)

        mask = (
            (df["datetime"] >= start_date)
            &
            (df["datetime"] <= end_date)
        )

        return df.loc[mask].reset_index(drop=True)

    # =====================================================
    # Dataset Information
    # =====================================================

    @staticmethod
    def summary(df: pd.DataFrame):

        print("=" * 70)
        print("DATASET SUMMARY")
        print("=" * 70)

        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")

        print("\nColumns")

        for column in df.columns:
            print(f" - {column}")

        print()

        print(df.head())

    # =====================================================
    # Close Connection
    # =====================================================

    def close(self):
        self.engine.close()


# ==========================================================
# Demo
# ==========================================================

if __name__ == "__main__":

    loader = DatasetLoader()

    dataset = loader.prepare_dataset(
        target="aqi"
    )

    loader.summary(dataset)

    loader.close()