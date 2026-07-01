"""
wbpcb.py

WBPCB Historical Data Connector

This connector reads historical WBPCB air quality datasets
from Excel files and returns standardized pandas DataFrames.

Responsibilities
----------------
✓ Discover WBPCB Excel files
✓ Read Excel files
✓ Normalize column names
✓ Perform basic structural validation

Not Responsible For
-------------------
✗ Data cleaning
✗ Duplicate removal
✗ Missing value handling
✗ Metadata registration
✗ Parquet generation
✗ Lakehouse operations
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from .base import BaseConnector
from .common import ConnectorUtils
from .registry import registry


class WBPCBConnector(BaseConnector):
    """
    Connector for historical WBPCB air-quality datasets.
    """

    def connect(self) -> None:
        """
        Verify source directory exists.
        """

        if not self.source.exists():
            raise FileNotFoundError(
                f"WBPCB source directory not found: {self.source}"
            )

    # =====================================================
    # File Discovery
    # =====================================================

    def discover(self) -> List[Path]:
        """
        Discover WBPCB Excel files.
        """

        files = ConnectorUtils.discover_files(
            self.source,
            extensions=["xlsx", "xls"],
            recursive=False,
        )

        return [
            file
            for file in files
            if not file.name.lower().startswith("~$")
        ]

    # =====================================================
    # Read Dataset
    # =====================================================

    def read(
        self,
        resource: Path | str,
    ) -> pd.DataFrame:
        """
        Read a WBPCB Excel file.
        """

        df = ConnectorUtils.read_excel(resource)

        df = ConnectorUtils.normalize_columns(df)

        self.validate(df)

        return df

    # =====================================================
    # Validation
    # =====================================================

    def validate(self, df: pd.DataFrame) -> bool:
        """
        Perform only basic structural validation.

        The connector should not enforce dataset-specific
        schemas. Column mapping and standardization are
        handled later by the ingestion and processing layers.
        """

        ConnectorUtils.validate_dataframe(df)

        return True

    # =====================================================
    # Batch Read
    # =====================================================

    def read_all(self) -> dict[str, pd.DataFrame]:
        """
        Read every discovered WBPCB dataset.

        Returns
        -------
        dict
            filename -> dataframe
        """

        datasets = {}

        for file in self.discover():
            datasets[file.stem] = self.read(file)

        return datasets

    # =====================================================
    # Close
    # =====================================================

    def close(self) -> None:
        """
        File-based connector.
        Nothing to close.
        """

        return None


# ==========================================================
# Register Connector
# ==========================================================

registry.register(
    "wbpcb",
    WBPCBConnector,
)