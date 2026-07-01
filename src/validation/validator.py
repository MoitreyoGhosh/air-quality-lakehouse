"""
validator.py
=====================================

Validation Engine

This module applies validation rules to canonical
environmental datasets.

Pipeline
--------
Canonical DataFrame
        │
        ▼
Validation Rules
        │
        ▼
Validation Results

Responsibilities
----------------
✓ Validate required columns
✓ Validate numeric columns
✓ Validate coordinate ranges
✓ Detect duplicate records
✓ Compute null statistics
✓ Validate measurement ranges

Not Responsible For
-------------------
✗ Data cleaning
✗ Data correction
✗ Reporting
✗ Storage
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from .rules import ValidationRules


class DataValidator:
    """
    Validation engine for canonical datasets.
    """

    def __init__(self) -> None:
        self.rules = ValidationRules()

    # =====================================================
    # Required Columns
    # =====================================================

    def validate_required_columns(
        self,
        df: pd.DataFrame,
        dataset_type: str,
    ) -> list[str]:
        """
        Return missing required columns.
        """

        required = self.rules.required_columns(dataset_type)

        return [
            column
            for column in required
            if column not in df.columns
        ]

    # =====================================================
    # Numeric Columns
    # =====================================================

    def validate_numeric_columns(
        self,
        df: pd.DataFrame,
        dataset_type: str,
    ) -> list[str]:
        """
        Return numeric columns that have non-numeric dtype.
        """

        invalid = []

        for column in self.rules.numeric_columns(dataset_type):

            if column not in df.columns:
                continue

            if not pd.api.types.is_numeric_dtype(df[column]):
                invalid.append(column)

        return invalid

    # =====================================================
    # Coordinate Validation
    # =====================================================

    def validate_coordinates(
        self,
        df: pd.DataFrame,
    ) -> dict[str, int]:
        """
        Count latitude/longitude values outside valid ranges.
        """

        result = {
            "latitude": 0,
            "longitude": 0,
        }

        if "latitude" in df.columns:

            low, high = self.rules.LATITUDE_RANGE

            result["latitude"] = int(
                (~df["latitude"].between(low, high)).sum()
            )

        if "longitude" in df.columns:

            low, high = self.rules.LONGITUDE_RANGE

            result["longitude"] = int(
                (~df["longitude"].between(low, high)).sum()
            )

        return result

    # =====================================================
    # Non-negative Measurements
    # =====================================================

    def validate_non_negative(
        self,
        df: pd.DataFrame,
    ) -> dict[str, int]:
        """
        Count negative values in non-negative columns.
        """

        result = {}

        for column in self.rules.NON_NEGATIVE:

            if column not in df.columns:
                continue

            result[column] = int(
                (df[column] < 0).sum()
            )

        return result

    # =====================================================
    # Percentage Columns
    # =====================================================

    def validate_percentages(
        self,
        df: pd.DataFrame,
    ) -> dict[str, int]:
        """
        Count percentage values outside valid ranges.
        """

        result = {}

        for column, (low, high) in self.rules.PERCENTAGE_COLUMNS.items():

            if column not in df.columns:
                continue

            result[column] = int(
                (~df[column].between(low, high)).sum()
            )

        return result

    # =====================================================
    # Duplicate Records
    # =====================================================

    def validate_duplicates(
        self,
        df: pd.DataFrame,
        dataset_type: str,
    ) -> int:
        """
        Count duplicate records based on dataset keys.
        """

        keys = self.rules.duplicate_keys(dataset_type)

        if not keys:
            return 0

        keys = [
            key
            for key in keys
            if key in df.columns
        ]

        if not keys:
            return 0

        return int(
            df.duplicated(subset=keys).sum()
        )

    # =====================================================
    # Null Statistics
    # =====================================================

    def null_summary(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Compute null counts and percentages.
        """

        summary = pd.DataFrame({
            "column": df.columns,
            "nulls": df.isna().sum().values,
        })

        summary["null_percent"] = (
            summary["nulls"] / len(df)
        ).round(4)

        return summary.sort_values(
            "null_percent",
            ascending=False,
        ).reset_index(drop=True)

    # =====================================================
    # Full Validation
    # =====================================================

    def validate(
        self,
        df: pd.DataFrame,
        dataset_type: str,
    ) -> dict[str, Any]:
        """
        Execute all validation checks.
        """

        return {
            "passed": True,
            "rows": len(df),
            "columns": len(df.columns),
            "missing_columns": self.validate_required_columns(
                df,
                dataset_type,
            ),
            "invalid_numeric_columns": self.validate_numeric_columns(
                df,
                dataset_type,
            ),
            "coordinate_errors": self.validate_coordinates(df),
            "negative_values": self.validate_non_negative(df),
            "percentage_errors": self.validate_percentages(df),
            "duplicate_rows": self.validate_duplicates(
                df,
                dataset_type,
            ),
            "null_summary": self.null_summary(df),
        }
    
    # =====================================================
    # Batch Validation
    # =====================================================
    
    def validate_all(
        self,
        datasets: dict[str, pd.DataFrame],
        dataset_type: str,
    ) -> dict[str, pd.DataFrame]:
        """
        Validate a collection of datasets.
    
        Parameters
        ----------
        datasets : dict[str, pd.DataFrame]
            Dictionary of canonical datasets.
    
        dataset_type : str
            Either "WBPCB" or "OPENMETEO".
    
        Returns
        -------
        dict[str, pd.DataFrame]
    
        Notes
        -----
        Validation does not modify the datasets.
        It only prints validation results and
        returns the original datasets.
        """
    
        print("=" * 80)
        print(f"{dataset_type} VALIDATION")
        print("=" * 80)
    
        for dataset_name, df in datasets.items():
        
            report = self.validate(
                df=df,
                dataset_type=dataset_type,
            )
    
            print(f"\nDataset : {dataset_name}")
            print(f"Rows    : {report['rows']}")
            print(f"Columns : {report['columns']}")
            print(f"Duplicate Rows : {report['duplicate_rows']}")
    
            if report["missing_columns"]:
                print(
                    "Missing Columns:",
                    report["missing_columns"],
                )
    
            if report["invalid_numeric_columns"]:
                print(
                    "Invalid Numeric Columns:",
                    report["invalid_numeric_columns"],
                )
    
        return datasets