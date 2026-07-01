"""
Generic Ingestion Manager for the
Environmental Intelligence Framework.

The Ingestion Manager coordinates all registered
connectors and provides a unified interface for
loading datasets into the framework.

Responsibilities
----------------
✓ Select connector
✓ Connect to source
✓ Discover datasets
✓ Read datasets
✓ Return DataFrames

Not Responsible For
-------------------
✗ Cleaning
✗ Validation
✗ Metadata
✗ Lakehouse operations
✗ Analytics
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from src.connectors.registry import registry
from src.connectors.base import BaseConnector


class IngestionManager:
    """
    Generic ingestion manager.

    Example
    -------
    >>> manager = IngestionManager()

    >>> datasets = manager.ingest(
    ...     connector_name="wbpcb",
    ...     source=RAW_DIR
    ... )
    """

    def __init__(self) -> None:
        pass

    # =====================================================
    # Connector Factory
    # =====================================================

    def get_connector(
        self,
        connector_name: str,
        source: str | Path,
    ) -> BaseConnector:
        """
        Create a connector instance.
        """

        return registry.create(
            connector_name,
            source=source,
        )

    # =====================================================
    # Ingest
    # =====================================================

    def ingest(
        self,
        connector_name: str,
        source: str | Path,
    ) -> Dict[str, pd.DataFrame]:
        """
        Read all datasets from a connector.

        Parameters
        ----------
        connector_name : str
            Registered connector name.

        source : str | Path
            Source directory.

        Returns
        -------
        dict[str, DataFrame]
        """

        connector = self.get_connector(
            connector_name,
            source,
        )

        connector.connect()

        datasets = connector.read_all()

        connector.close()

        return datasets

    # =====================================================
    # Summary
    # =====================================================

    @staticmethod
    def summary(
        datasets: Dict[str, pd.DataFrame],
    ) -> pd.DataFrame:
        """
        Return a summary of loaded datasets.
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

        return pd.DataFrame(rows)

    # =====================================================
    # Connector List
    # =====================================================

    @staticmethod
    def available_connectors():
        """
        Return registered connectors.
        """

        return registry.available()