"""
discover.py
=====================================

Schema Discovery Module

This module discovers schemas from datasets using registered
connectors.

Responsibilities
----------------
✓ Read datasets through connectors
✓ Collect raw column names
✓ Normalize discovered columns
✓ Generate schema summaries
✓ Compare schemas

Not Responsible For
-------------------
✗ Alias resolution
✗ Schema mapping
✗ Data validation
✗ Data transformation
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.connectors.registry import registry as connector_registry
from src.schema.normalize import ColumnNormalizer


class SchemaDiscovery:
    """
    Discover schemas from connector datasets.
    """

    # =====================================================
    # Discovery
    # =====================================================

    def discover(
        self,
        connector_name: str,
        source: str | Path,
    ) -> dict[str, dict[str, Any]]:
        """
        Discover schemas for all datasets exposed by a connector.

        Returns
        -------
        dict

        {
            dataset_name:
            {
                "raw": [...],
                "normalized": [...]
            }
        }
        """

        connector = connector_registry.create(
            connector_name,
            source=source,
        )

        connector.connect()

        datasets = connector.read_all()

        connector.close()

        discovered = {}

        for dataset_name, df in datasets.items():

            discovered[dataset_name] = {

                "raw": list(df.columns),

                "normalized":
                    ColumnNormalizer.normalize_columns(
                        df.columns
                    ),

            }

        return discovered

    # =====================================================
    # Common Columns
    # =====================================================

    @staticmethod
    def common_columns(
        discovered: dict,
    ) -> list[str]:
        """
        Columns present in every dataset.
        """

        if not discovered:
            return []

        column_sets = [

            set(schema["normalized"])

            for schema in discovered.values()

        ]

        return sorted(
            set.intersection(*column_sets)
        )

    # =====================================================
    # Unique Columns
    # =====================================================

    @staticmethod
    def unique_columns(
        discovered: dict,
    ) -> dict[str, list[str]]:
        """
        Columns unique to each dataset.
        """

        result = {}

        for dataset, schema in discovered.items():

            current = set(schema["normalized"])

            others = set()

            for name, other_schema in discovered.items():

                if name == dataset:
                    continue

                others.update(
                    other_schema["normalized"]
                )

            result[dataset] = sorted(
                current - others
            )

        return result

    # =====================================================
    # Summary
    # =====================================================

    @staticmethod
    def summary(
        discovered: dict,
    ) -> pd.DataFrame:
        """
        Dataset schema summary.
        """

        rows = []

        for dataset, schema in discovered.items():

            rows.append({

                "dataset": dataset,

                "columns":
                    len(schema["normalized"]),

                "raw_columns":
                    ", ".join(schema["raw"]),

                "normalized_columns":
                    ", ".join(schema["normalized"]),

            })

        return pd.DataFrame(rows)

    # =====================================================
    # Statistics
    # =====================================================

    @staticmethod
    def statistics(
        discovered: dict,
    ) -> dict:
        """
        Overall schema statistics.
        """

        unique_columns = {

            column

            for schema in discovered.values()

            for column in schema["normalized"]

        }

        return {

            "datasets":
                len(discovered),

            "unique_columns":
                len(unique_columns),

            "common_columns":
                len(
                    SchemaDiscovery.common_columns(
                        discovered
                    )
                ),

        }

    # =====================================================
    # Report
    # =====================================================

    @staticmethod
    def print_report(
        discovered: dict,
    ) -> None:
        """
        Print schema discovery report.
        """

        print("=" * 80)
        print("SCHEMA DISCOVERY REPORT")
        print("=" * 80)

        for dataset, schema in discovered.items():

            print(f"\nDataset : {dataset}")

            print("-" * 80)

            print("\nRaw Columns")

            print("-" * 40)

            for column in schema["raw"]:
                print(column)

            print("\nNormalized Columns")

            print("-" * 40)

            for column in schema["normalized"]:
                print(column)

        print("\n" + "=" * 80)

        print("Statistics")

        print("=" * 80)

        stats = SchemaDiscovery.statistics(
            discovered
        )

        for key, value in stats.items():

            print(f"{key:<20}: {value}")