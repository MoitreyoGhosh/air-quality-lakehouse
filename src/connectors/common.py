"""
Common utilities for all connectors in the
Environmental Intelligence Framework.

This module provides reusable helper functions for:

- File discovery
- Reading CSV/Excel files
- Basic dataframe validation
- Column normalization
- File information

Dataset-specific logic must NOT be implemented here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


class ConnectorUtils:
    """
    Generic utility methods shared by all connectors.
    """

    SUPPORTED_EXTENSIONS = {
        ".csv",
        ".xlsx",
        ".xls",
        ".parquet",
    }

    # =====================================================
    # File Discovery
    # =====================================================

    @staticmethod
    def discover_files(
        directory: str | Path,
        extensions: Iterable[str] | None = None,
        recursive: bool = True,
    ) -> list[Path]:
        """
        Discover files inside a directory.

        Parameters
        ----------
        directory : str | Path
            Directory to search.

        extensions : Iterable[str], optional
            Allowed file extensions.

        recursive : bool, default=True
            Search subdirectories recursively.

        Returns
        -------
        list[Path]
        """

        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        if extensions is None:
            extensions = ConnectorUtils.SUPPORTED_EXTENSIONS

        extensions = {
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in extensions
        }

        iterator = (
            directory.rglob("*")
            if recursive
            else directory.glob("*")
        )

        files = [
            file
            for file in iterator
            if file.is_file()
            and file.suffix.lower() in extensions
        ]

        return sorted(files)

    # =====================================================
    # Readers
    # =====================================================

    @staticmethod
    def read_excel(path: str | Path, **kwargs) -> pd.DataFrame:
        """
        Read an Excel file.
        """

        return pd.read_excel(path, **kwargs)

    @staticmethod
    def read_csv(path: str | Path, **kwargs) -> pd.DataFrame:
        """
        Read a CSV file.
        """

        return pd.read_csv(path, **kwargs)

    @staticmethod
    def read_parquet(path: str | Path, **kwargs) -> pd.DataFrame:
        """
        Read a Parquet file.
        """

        return pd.read_parquet(path, **kwargs)

    # =====================================================
    # DataFrame Validation
    # =====================================================

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> None:
        """
        Basic structural validation.

        Raises
        ------
        ValueError
        """

        if df is None:
            raise ValueError("DataFrame is None.")

        if df.empty:
            raise ValueError("DataFrame is empty.")

        if len(df.columns) == 0:
            raise ValueError("No columns found.")

    @staticmethod
    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names.

        Example:
            Temperature (°C)
            →

            temperature_c
        """

        df = df.copy()

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
            .str.replace("/", "_", regex=False)
            .str.replace("(", "", regex=False)
            .str.replace(")", "", regex=False)
        )

        return df

    @staticmethod
    def convert_datetime(
        df: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:
        """
        Convert a column to datetime.
        """

        df = df.copy()

        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

        return df

    # =====================================================
    # File Metadata
    # =====================================================

    @staticmethod
    def file_metadata(path: str | Path) -> dict:
        """
        Return basic file metadata.
        """

        path = Path(path)

        stat = path.stat()

        return {
            "name": path.name,
            "stem": path.stem,
            "extension": path.suffix,
            "size_bytes": stat.st_size,
            "parent": str(path.parent),
        }

    # =====================================================
    # Generic Summary
    # =====================================================

    @staticmethod
    def dataframe_summary(df: pd.DataFrame) -> dict:
        """
        Return a lightweight dataframe summary.
        """

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicates": int(df.duplicated().sum()),
        }