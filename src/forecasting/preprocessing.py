"""
preprocessing.py

Data preprocessing and feature engineering
for environmental forecasting.
"""

from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class DataPreprocessor:
    """
    Prepares datasets for machine learning.
    """

    def __init__(self):
        self.station_encoder = LabelEncoder()

    # =====================================================
    # Feature Engineering
    # =====================================================

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create useful time-based features.
        """

        df = df.copy()

        df["datetime"] = pd.to_datetime(df["datetime"])

        df["year"] = df["datetime"].dt.year
        df["month"] = df["datetime"].dt.month
        df["day"] = df["datetime"].dt.day
        df["hour"] = df["datetime"].dt.hour
        df["day_of_week"] = df["datetime"].dt.dayofweek
        df["week_of_year"] = (
            df["datetime"]
            .dt.isocalendar()
            .week
            .astype(int)
        )

        if "station_name" in df.columns:
            df["station"] = self.station_encoder.fit_transform(
                df["station_name"]
            )

        return df

    # =====================================================
    # Lag Features
    # =====================================================

    def create_lag_features(
        self,
        df: pd.DataFrame,
        target: str,
        lags=(1, 3, 6, 12, 24),
    ) -> pd.DataFrame:

        df = df.copy()

        for lag in lags:
            df[f"{target}_lag_{lag}"] = (
                df.groupby("station_id")[target]
                .shift(lag)
            )

        return df

    # =====================================================
    # Rolling Statistics
    # =====================================================

    def create_rolling_features(
        self,
        df: pd.DataFrame,
        target: str,
        windows=(3, 6, 12, 24),
    ) -> pd.DataFrame:

        df = df.copy()

        for window in windows:

            df[f"{target}_rolling_mean_{window}"] = (
                df.groupby("station_id")[target]
                .transform(
                    lambda x: x.rolling(window).mean()
                )
            )

            df[f"{target}_rolling_std_{window}"] = (
                df.groupby("station_id")[target]
                .transform(
                    lambda x: x.rolling(window).std()
                )
            )

        return df

    # =====================================================
    # Missing Values
    # =====================================================

    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        df = df.ffill()
        df = df.bfill()
        df = df.dropna()

        return df

    # =====================================================
    # Train/Test Split
    # =====================================================

    @staticmethod
    def split(
        df: pd.DataFrame,
        target: str,
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> Tuple:

        # Separate features and target
        X = df.drop(columns=[target]).copy()

        # Remove columns unsuitable for scikit-learn
        columns_to_drop = [
            "datetime",
            "station_id",
            "station_name",
        ]

        X = X.drop(
            columns=[
                col
                for col in columns_to_drop
                if col in X.columns
            ],
            errors="ignore",
        )

        # Keep only numeric columns
        X = X.select_dtypes(include=["number"])

        y = df[target]

        return train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            shuffle=False,
        )

    # =====================================================
    # Complete Pipeline
    # =====================================================

    def process(
        self,
        df: pd.DataFrame,
        target: str,
    ):

        df = self.engineer_features(df)
        df = self.create_lag_features(df, target)
        df = self.create_rolling_features(df, target)
        df = self.clean(df)

        return self.split(df, target)


# =====================================================
# Demo
# =====================================================

if __name__ == "__main__":

    from src.forecasting.dataset import DatasetLoader

    loader = DatasetLoader()

    df = loader.prepare_dataset(target="aqi")

    pre = DataPreprocessor()

    X_train, X_test, y_train, y_test = pre.process(
        df,
        target="aqi",
    )

    print("=" * 60)
    print("Preprocessing Successful")
    print("=" * 60)

    print("Training Features :", X_train.shape)
    print("Testing Features  :", X_test.shape)
    print("Training Target   :", y_train.shape)
    print("Testing Target    :", y_test.shape)

    print("\nFeature Columns:")
    print(X_train.columns.tolist())