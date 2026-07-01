"""
Abstract base class for all data connectors.

Every connector in the Environmental Intelligence
Framework must inherit from BaseConnector.

Responsibilities
----------------
✓ Connect to a data source
✓ Discover available datasets
✓ Read datasets
✓ Perform basic structural validation
✓ Return pandas DataFrames

A connector MUST NOT:
---------------------
✗ Transform data
✗ Clean data
✗ Remove duplicates
✗ Generate Parquet
✗ Register metadata
✗ Write to DuckDB
✗ Execute analytics
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

import pandas as pd


class BaseConnector(ABC):
    """
    Abstract connector interface.

    Every connector must implement this interface so that the
    ingestion layer can interact with any data source in a
    consistent manner.
    """

    def __init__(self, source: Path | str):
        self.source = Path(source)

    @abstractmethod
    def connect(self) -> None:
        """
        Initialize the connection to the data source.

        For file-based connectors this may simply verify that
        the source path exists.

        For API or database connectors this should establish
        the connection/session.
        """
        raise NotImplementedError

    @abstractmethod
    def discover(self) -> List[Path]:
        """
        Discover available datasets.

        Returns
        -------
        List[Path]
            List of files/resources available for ingestion.
        """
        raise NotImplementedError

    @abstractmethod
    def read(self, resource: Path | str) -> pd.DataFrame:
        """
        Read a dataset.

        Parameters
        ----------
        resource : Path | str
            Dataset to read.

        Returns
        -------
        pandas.DataFrame
        """
        raise NotImplementedError

    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        """
        Perform basic structural validation.

        Validation here should only verify that:

        - dataframe exists
        - dataframe is not empty
        - columns are present

        Business validation belongs to the Validation layer.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """
        Close the connection if required.

        File connectors generally don't need to do anything.

        Database/API connectors should release resources.
        """
        raise NotImplementedError

    # -----------------------------------------------------
    # Common Helper Methods
    # -----------------------------------------------------

    @staticmethod
    def is_empty(df: Optional[pd.DataFrame]) -> bool:
        """
        Check whether a dataframe is empty.

        Parameters
        ----------
        df : pandas.DataFrame | None

        Returns
        -------
        bool
        """
        return df is None or df.empty

    @staticmethod
    def has_columns(
        df: pd.DataFrame,
        required_columns: List[str],
    ) -> bool:
        """
        Verify required columns exist.

        Parameters
        ----------
        df : pandas.DataFrame
        required_columns : list[str]

        Returns
        -------
        bool
        """
        return all(column in df.columns for column in required_columns)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(source='{self.source}')"
        )