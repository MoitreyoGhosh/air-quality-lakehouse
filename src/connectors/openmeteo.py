"""
openmeteo.py

Open-Meteo Connector

This connector is responsible for reading historical
Open-Meteo weather datasets.

Future versions of this connector will also support
real-time API ingestion using the same interface.

Responsibilities
----------------
✓ Discover weather datasets
✓ Read Excel files
✓ Normalize column names
✓ Basic structural validation

Not Responsible For
-------------------
✗ Data cleaning
✗ Metadata registration
✗ Lakehouse operations
✗ Validation reports
✗ Feature engineering
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from .base import BaseConnector
from .common import ConnectorUtils
from .registry import registry


class OpenMeteoConnector(BaseConnector):
    """
    Connector for Open-Meteo weather datasets.
    """

    def connect(self) -> None:
        """
        Verify source directory exists.
        """

        if not self.source.exists():
            raise FileNotFoundError(
                f"Source directory not found: {self.source}"
            )

    # =====================================================
    # File Discovery
    # =====================================================

    def discover(self) -> List[Path]:
        """
        Discover Open-Meteo Excel files.
        """

        files = ConnectorUtils.discover_files(
            self.source,
            extensions=["xlsx", "xls"],
            recursive=True,
        )

        return [
            file
            for file in files
            if not file.name.startswith("~$")
        ]

    # =====================================================
    # Read Dataset
    # =====================================================

    def read(
        self,
        resource: Path | str,
    ) -> pd.DataFrame:
        """
        Read a weather dataset.
        """

        df = ConnectorUtils.read_excel(resource)

        df = ConnectorUtils.normalize_columns(df)

        self.validate(df)

        return df

    # =====================================================
    # Validation
    # =====================================================

    def validate(
        self,
        df: pd.DataFrame,
    ) -> bool:
        """
        Perform only structural validation.

        The connector should never assume the source schema.
        Schema discovery and mapping are handled later by the
        Schema layer.
        """

        ConnectorUtils.validate_dataframe(df)

        return True

    # =====================================================
    # Batch Read
    # =====================================================

    def read_all(self) -> dict[str, pd.DataFrame]:
        """
        Read every discovered dataset.
        """

        datasets = {}

        for file in self.discover():
            datasets[file.stem] = self.read(file)

        return datasets

    # =====================================================
    # Placeholder for Future API Support
    # =====================================================

    def fetch_realtime(self, *args, **kwargs):
        """
        Placeholder for real-time API ingestion.

        This method will be implemented during the
        Real-time Ingestion phase.
        """

        raise NotImplementedError(
            "Realtime API ingestion will be implemented "
            "in Phase 2."
        )

    # =====================================================
    # Close
    # =====================================================

    def close(self) -> None:
        """
        File-based connector.
        """

        return None


# ==========================================================
# Register Connector
# ==========================================================

registry.register(
    "openmeteo",
    OpenMeteoConnector,
)