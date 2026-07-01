"""
report.py
=====================================

Validation Reporting

This module converts validation results into
human-readable summaries and tabular reports.

Pipeline
--------
DataValidator
        │
        ▼
Validation Result
        │
        ▼
Validation Report

Responsibilities
----------------
✓ Generate validation summaries
✓ Produce tabular reports
✓ Pretty-print validation results

Not Responsible For
-------------------
✗ Executing validation
✗ Data cleaning
✗ Storage
"""

from __future__ import annotations

from typing import Any

import pandas as pd


class ValidationReport:
    """
    Utility class for formatting validation results.
    """

    # =====================================================
    # Summary
    # =====================================================

    @staticmethod
    def summary(result: dict[str, Any]) -> pd.DataFrame:
        """
        Return a one-row summary table.
        """

        return pd.DataFrame(
            [
                {
                    "rows": result["rows"],
                    "columns": result["columns"],
                    "missing_columns": len(result["missing_columns"]),
                    "invalid_numeric": len(
                        result["invalid_numeric_columns"]
                    ),
                    "duplicate_rows": result["duplicate_rows"],
                    "coordinate_errors": sum(
                        result["coordinate_errors"].values()
                    ),
                    "negative_values": sum(
                        result["negative_values"].values()
                    ),
                    "percentage_errors": sum(
                        result["percentage_errors"].values()
                    ),
                }
            ]
        )

    # =====================================================
    # Issues
    # =====================================================

    @staticmethod
    def issues(result: dict[str, Any]) -> pd.DataFrame:
        """
        Return detected validation issues.
        """

        issues = []

        # Missing columns
        for column in result["missing_columns"]:
            issues.append(
                {
                    "category": "Missing Column",
                    "field": column,
                    "count": None,
                }
            )

        # Invalid numeric columns
        for column in result["invalid_numeric_columns"]:
            issues.append(
                {
                    "category": "Invalid Numeric Type",
                    "field": column,
                    "count": None,
                }
            )

        # Coordinate errors
        for column, count in result["coordinate_errors"].items():
            if count > 0:
                issues.append(
                    {
                        "category": "Coordinate Range",
                        "field": column,
                        "count": count,
                    }
                )

        # Negative values
        for column, count in result["negative_values"].items():
            if count > 0:
                issues.append(
                    {
                        "category": "Negative Values",
                        "field": column,
                        "count": count,
                    }
                )

        # Percentage errors
        for column, count in result["percentage_errors"].items():
            if count > 0:
                issues.append(
                    {
                        "category": "Percentage Range",
                        "field": column,
                        "count": count,
                    }
                )

        # Duplicate rows
        if result["duplicate_rows"] > 0:
            issues.append(
                {
                    "category": "Duplicate Rows",
                    "field": "-",
                    "count": result["duplicate_rows"],
                }
            )

        return pd.DataFrame(issues)

    # =====================================================
    # Null Report
    # =====================================================

    @staticmethod
    def null_report(result: dict[str, Any]) -> pd.DataFrame:
        """
        Return null statistics.
        """

        return result["null_summary"].copy()

    # =====================================================
    # Console Report
    # =====================================================

    @classmethod
    def print_report(
        cls,
        dataset_name: str,
        result: dict[str, Any],
    ) -> None:
        """
        Pretty-print validation report.
        """

        print("=" * 80)
        print("VALIDATION REPORT")
        print("=" * 80)

        print(f"Dataset : {dataset_name}")
        print(f"Rows    : {result['rows']}")
        print(f"Columns : {result['columns']}")

        print("\nSummary")
        print("-" * 80)
        print(cls.summary(result))

        issues = cls.issues(result)

        print("\nIssues")
        print("-" * 80)

        if issues.empty:
            print("No validation issues detected.")
        else:
            print(issues)

        print("\nNull Summary")
        print("-" * 80)
        print(cls.null_report(result))