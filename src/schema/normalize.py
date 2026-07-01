"""
normalize.py
=====================================

Generic Column Normalization Utilities

Responsibilities
----------------
✓ Normalize raw column names
✓ Remove units and symbols
✓ Convert to snake_case
✓ Standardize naming format

This module DOES NOT perform semantic mapping.
That responsibility belongs to aliases.py.

Examples
--------
PM 2.5 Avg µg m³
    -> pm_2_5_avg

Temperature_2m_°C
    -> temperature_2m

Relative Humidity 2m %
    -> relative_humidity_2m

Wind Speed Avg
    -> wind_speed_avg
"""

from __future__ import annotations

import re
import unicodedata
from typing import Iterable

import pandas as pd


class ColumnNormalizer:
    """
    Generic lexical column normalizer.

    This class converts heterogeneous column names into a
    consistent snake_case representation while preserving
    their semantic meaning.

    No dataset-specific mapping is performed here.
    """

    # ---------------------------------------------

    UNITS = [
        "µg",
        "ug",
        "μg",
        "°c",
        "°",
        "%",
        "km/h",
        "km h",
        "hpa",
        "mm",
    ]

    # ---------------------------------------------

    @classmethod
    def normalize(cls, column: str) -> str:
        """
        Normalize a single column name into a clean snake_case
        lexical representation.

        No semantic mapping is performed here.
        """

        column = str(column).strip().lower()

        # --------------------------------------------------
        # Preserve decimal notation before punctuation removal
        # --------------------------------------------------

        column = column.replace("2.5", "2_5")

        # --------------------------------------------------
        # Remove units BEFORE unicode normalization
        # --------------------------------------------------

        units = [
            "µg m³",
            "μg/m³",
            "μg m3",
            "µg",
            "μg",
            "ug",
            "m³",
            "m3",
            "°c",
            "°",
            "µg/m³",
            "%",
            "km/h",
            "km h",
            "mm",
            "hpa",
        ]

        for unit in units:
            column = column.replace(unit, "")
    
        # --------------------------------------------------
        # Unicode normalization
        # --------------------------------------------------
    
        column = unicodedata.normalize("NFKD", column)
        column = column.encode("ascii", "ignore").decode()
    
        # --------------------------------------------------
        # Replace separators
        # --------------------------------------------------
    
        column = re.sub(r"[ /\\\-]+", "_", column)
    
        # Remove brackets
        column = re.sub(r"[\(\)\[\]\{\}]", "", column)
    
        # Remove remaining punctuation except underscore
        column = re.sub(r"[^a-z0-9_]", "", column)
    
        # Collapse underscores
        column = re.sub(r"_+", "_", column)
    
        column = column.strip("_")
    
        return column
    
    # ---------------------------------------------

    @classmethod
    def normalize_columns(
        cls,
        columns: Iterable,
    ) -> list[str]:
        """
        Normalize multiple columns.
        """

        return [
            cls.normalize(column)
            for column in columns
        ]

    # ---------------------------------------------

    @classmethod
    def normalize_dataframe(
        cls,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Return a dataframe with normalized columns.
        """

        df = df.copy()

        df.columns = cls.normalize_columns(df.columns)

        return df