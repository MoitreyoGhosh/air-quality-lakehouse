"""
historical.py
=====================================

Historical Data Ingestion

This module orchestrates the ingestion of historical datasets
using registered connectors and the schema pipeline.

Pipeline
--------
Connector
    ↓
Read DataFrames
    ↓
Schema Mapper
    ↓
Canonical DataFrames
    ↓
Return to downstream pipeline

Responsibilities
----------------
✓ Instantiate connectors
✓ Read historical datasets
✓ Apply schema mapping
✓ Return canonical DataFrames
✓ Generate ingestion summaries

Not Responsible For
-------------------
✗ Data cleaning
✗ Missing value handling
✗ Validation
✗ Bronze/Silver/Gold storage
✗ Metadata registration
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.connectors.registry import registry as connector_registry
from src.schema.mapper import SchemaMapper


class HistoricalIngestion:
    """
    Historical ingestion pipeline.
    """

    def __init__(self) -> None:

        self.mapper = SchemaMapper()

    # =====================================================
    # Read
    # =====================================================

    def read(
        self,
        connector_name: str,
        source: str | Path,
    ) -> dict[str, pd.DataFrame]:
        """
        Read datasets using a registered connector.
        """

        connector = connector_registry.create(
            connector_name,
            source=source,
        )

        connector.connect()

        try:
            datasets = connector.read_all()
        finally:
            connector.close()

        return datasets

    # =====================================================
    # Standardize
    # =====================================================

    def standardize(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> dict[str, pd.DataFrame]:
        """
        Convert datasets to the framework's canonical schema.
        """

        standardized = {}

        for name, df in datasets.items():

            mapped_df, _ = self.mapper.map(df)

            standardized[name] = mapped_df

        return standardized

    # =====================================================
    # Ingest
    # =====================================================

    def ingest(
        self,
        connector_name: str,
        source: str | Path,
    ) -> dict[str, pd.DataFrame]:
        """
        Execute the historical ingestion pipeline.
        """

        datasets = self.read(
            connector_name=connector_name,
            source=source,
        )

        datasets = self.standardize(datasets)

        return datasets

    # =====================================================
    # Summary
    # =====================================================

    @staticmethod
    def summary(
        datasets: dict[str, pd.DataFrame],
    ) -> pd.DataFrame:
        """
        Generate a summary of ingested datasets.
        """

        rows = []

        for name, df in datasets.items():

            rows.append(
                {
                    "dataset": name,
                    "rows": len(df),
                    "columns": len(df.columns),
                }
            )

        return (
            pd.DataFrame(rows)
            .sort_values("dataset")
            .reset_index(drop=True)
        )