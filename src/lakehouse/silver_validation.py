"""
silver_validation.py
=====================================

Silver Layer Validation

Responsibilities
----------------
✓ Validate Silver Master datasets
✓ Structural validation
✓ Duplicate validation
✓ Missing value validation
✓ Source agreement validation
✓ Generate validation reports
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)

from src.database.utils import DatabaseUtils


class SilverValidator:

    """
    Silver Validation Framework
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        self.project_root = Path.cwd()

        self.report_directory = (
            self.project_root
            / "reports"
            / "silver_validation"
        )

        self.report_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =====================================================
    # Load Silver Tables
    # =====================================================

    @staticmethod
    def load_wbpcb():

        return DatabaseUtils.query(
            """
            SELECT *
            FROM silver.wbpcb_master
            """
        )

    @staticmethod
    def load_weather():

        return DatabaseUtils.query(
            """
            SELECT *
            FROM silver.weather_master
            """
        )

    @staticmethod
    def load_environment():

        return DatabaseUtils.query(
            """
            SELECT *
            FROM silver.environment_master
            """
        )

    # =====================================================
    # Dataset Summary
    # =====================================================

    @staticmethod
    def dataset_summary(
        name: str,
        df: pd.DataFrame,
    ) -> dict:

        duplicates = 0

        if (
            "station_id" in df.columns
            and "datetime" in df.columns
        ):

            duplicates = int(
                df.duplicated(
                    subset=[
                        "station_id",
                        "datetime",
                    ]
                ).sum()
            )

        return {

            "dataset": name,

            "rows": len(df),

            "columns": len(df.columns),

            "stations": (
                df["station_id"].nunique()
                if "station_id" in df.columns
                else np.nan
            ),

            "start_datetime": (
                df["datetime"].min()
                if "datetime" in df.columns
                else np.nan
            ),

            "end_datetime": (
                df["datetime"].max()
                if "datetime" in df.columns
                else np.nan
            ),

            "duplicates": duplicates,

            "missing_values": int(
                df.isna().sum().sum()
            ),

        }

    # =====================================================
    # Missing Summary
    # =====================================================

    @staticmethod
    def missing_summary(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        report = pd.DataFrame({

            "column": df.columns,

            "missing": df.isna().sum().values,

            "percentage": (
                df.isna().mean().values
                * 100
            ),

            "dtype": df.dtypes.astype(str).values,

        })

        return report.sort_values(
            "missing",
            ascending=False,
        )

    # =====================================================
    # Source Agreement
    # =====================================================

    @staticmethod
    def source_agreement(
        wbpcb: pd.DataFrame,
        weather: pd.DataFrame,
    ) -> pd.DataFrame:

        exclude = {
            "station_id",
            "station_name",
            "district",
            "latitude",
            "longitude",
            "datetime",
            "aqi",
            "pm25",
            "pm10",
            "wind_speed_min",
            "wind_speed_max",
        }

        compare_columns = sorted(
            (
                set(wbpcb.columns)
                & set(weather.columns)
            )
            - exclude
        )

        merged = wbpcb.merge(

            weather,
            on=[
                "station_id",
                "datetime",
            ],
            suffixes=(
                "_wbpcb",
                "_weather",
            ),
            how="inner",
        )

        report = []

        for variable in compare_columns:

            left = f"{variable}_wbpcb"
            right = f"{variable}_weather"

            if (
                left not in merged.columns
                or right not in merged.columns
            ):
                continue

            data = merged[
                [
                    left,
                    right,
                ]
            ].dropna()

            if len(data) == 0:
                continue

            y_true = data[left].astype(float)
            y_pred = data[right].astype(float)

            # -------------------------------------------------
            # Unit Conversion
            # -------------------------------------------------

            if variable == "wind_speed":
            
                # Open-Meteo is stored in km/h
                # WBPCB is stored in m/s
                # Convert Open-Meteo -> m/s

                y_pred = y_pred / 3.6

            # -------------------------------------------------
            # Circular Wind Direction
            # -------------------------------------------------

            if variable == "wind_direction":
                angle_diff = np.abs(y_true - y_pred)
                diff = np.minimum(
                    angle_diff,
                    360 - angle_diff,
                )
                mae = diff.mean()
                rmse = np.sqrt(
                    np.mean(diff ** 2)
                )
                bias = (
                    y_true - y_pred
                ).mean()
                correlation = np.nan
                min_diff = diff.min()
                max_diff = diff.max()
                std_diff = diff.std()

            else:
                diff = y_true - y_pred
                mae = mean_absolute_error(
                    y_true,
                    y_pred,
                )
                rmse = np.sqrt(
                    mean_squared_error(
                        y_true,
                        y_pred,
                    )
                )
                bias = diff.mean()
                correlation = y_true.corr(
                    y_pred
                )
                min_diff = diff.min()
                max_diff = diff.max()
                std_diff = diff.std()

            report.append({
                "variable": variable,
                "samples": len(data),
                "mae": mae,
                "rmse": rmse,
                "bias": bias,
                "correlation": correlation,
                "min_difference": min_diff,
                "max_difference": max_diff,
                "std_difference": std_diff,

            })
        return pd.DataFrame(report)

    # =====================================================
    # Save CSV
    # =====================================================

    def save_csv(
        self,
        name: str,
        df: pd.DataFrame,
    ):

        path = (
            self.report_directory
            / f"{name}.csv"
        )

        df.to_csv(
            path,
            index=False,
        )

        print(
            f"✓ Saved {path.name}"
        )

    # =====================================================
    # Validate
    # =====================================================

    def validate(self):

        print("=" * 80)
        print("SILVER VALIDATION")
        print("=" * 80)

        wbpcb = self.load_wbpcb()

        weather = self.load_weather()

        environment = self.load_environment()

        # -------------------------------------------------
        # Dataset Summary
        # -------------------------------------------------

        summary = pd.DataFrame([

            self.dataset_summary(
                "WBPCB Master",
                wbpcb,
            ),

            self.dataset_summary(
                "Weather Master",
                weather,
            ),

            self.dataset_summary(
                "Environment Master",
                environment,
            ),

        ])

        self.save_csv(
            "validation_summary",
            summary,
        )

        # -------------------------------------------------
        # Missing Values
        # -------------------------------------------------

        missing_reports = []

        for name, df in [

            ("wbpcb_master", wbpcb),

            ("weather_master", weather),

            ("environment_master", environment),

        ]:

            report = self.missing_summary(df)

            report.insert(
                0,
                "dataset",
                name,
            )

            missing_reports.append(
                report
            )

        missing = pd.concat(
            missing_reports,
            ignore_index=True,
        )

        self.save_csv(
            "missing_values",
            missing,
        )

        # -------------------------------------------------
        # Source Agreement
        # -------------------------------------------------

        agreement = self.source_agreement(
            wbpcb,
            weather,
        )

        if not agreement.empty:
        
            print()
            print("Source Agreement Summary")
            print("-" * 80)

            for _, row in agreement.iterrows():
                if row["variable"] == "wind_speed":
                    print(
                        f"{row['variable']:<18}"
                        "(WBPCB m/s vs OM km/h→m/s) "
                        f"MAE={row['mae']:.3f}  "
                        f"RMSE={row['rmse']:.3f}  "
                        f"Bias={row['bias']:.3f}  "
                        f"r={row['correlation']:.3f}"
                    )

                elif row["variable"] == "wind_direction":
                    print(
                        f"{row['variable']:<18}"
                        "(Circular Error) "
                        f"MAE={row['mae']:.3f}  "
                        f"RMSE={row['rmse']:.3f}"
                    )

                else:
                    print(
                        f"{row['variable']:<18}"
                        f"MAE={row['mae']:.3f}  "
                        f"RMSE={row['rmse']:.3f}  "
                        f"Bias={row['bias']:.3f}  "
                        f"r={row['correlation']:.3f}"
                    )

        self.save_csv(
            "source_agreement_report",
            agreement,
        )

        # -------------------------------------------------
        # Console Summary
        # -------------------------------------------------

        print()
        print("=" * 80)
        print("DATASET SUMMARY")
        print("=" * 80)
        print(summary)
        print()
        print("=" * 80)
        print("SOURCE AGREEMENT")
        print("=" * 80)
        if agreement.empty:
            print(
                "No overlapping weather variables found."
            )
        else:
            print(
                agreement.round(4)
            )
        print()
        print("=" * 80)
        print("VALIDATION COMPLETE")
        print("=" * 80)
        
        return {
            "summary": summary,
            "missing": missing,
            "source_agreement": agreement,
        }

    # =====================================================
    # Run
    # =====================================================

    def run(self):

        results = self.validate()

        return results

# ==========================================================
# Singleton
# ==========================================================

silver_validator = SilverValidator()

# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    silver_validator.run()