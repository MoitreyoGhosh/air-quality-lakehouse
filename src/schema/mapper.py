"""
mapper.py
=====================================

Schema Mapper

The Schema Mapper converts heterogeneous source schemas
into the framework's canonical schema.

Pipeline
--------
Raw DataFrame
        │
        ▼
ColumnNormalizer
        │
        ▼
AliasResolver
        │
        ▼
Canonical DataFrame

Responsibilities
----------------
✓ Normalize column names
✓ Resolve semantic aliases
✓ Produce canonical DataFrames
✓ Report schema changes

Not Responsible For
-------------------
✗ Data validation
✗ Feature engineering
✗ Data cleaning
✗ Type conversion
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .normalize import ColumnNormalizer
from .aliases import AliasResolver


# ==========================================================
# Mapping Report
# ==========================================================

@dataclass
class MappingReport:
    """
    Stores information about a schema mapping operation.
    """

    original_columns: list[str]

    normalized_columns: list[str]

    canonical_columns: list[str]

    renamed_columns: dict[str, str]


# ==========================================================
# Schema Mapper
# ==========================================================

class SchemaMapper:
    """
    Generic schema mapper.

    This class performs schema normalization and alias
    resolution for any environmental dataset.
    """

    # ------------------------------------------------------

    def normalize(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize column names.
        """

        return ColumnNormalizer.normalize_dataframe(df)

    # ------------------------------------------------------

    def resolve(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Resolve normalized columns to canonical names.
        """

        return AliasResolver.resolve_dataframe(df)

    # ------------------------------------------------------

    def map(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, MappingReport]:
        """
        Convert a dataframe to the framework's canonical schema.

        Returns
        -------
        (dataframe, MappingReport)
        """

        original = list(df.columns)

        normalized_df = self.normalize(df)

        normalized = list(normalized_df.columns)

        canonical_df = self.resolve(normalized_df)

        canonical = list(canonical_df.columns)

        report = MappingReport(
            original_columns=original,
            normalized_columns=normalized,
            canonical_columns=canonical,
            renamed_columns={
                old: new
                for old, new in zip(original, canonical)
                if old != new
            },
        )

        return canonical_df, report

    # ------------------------------------------------------

    def report(
        self,
        report: MappingReport,
    ) -> pd.DataFrame:
        """
        Produce a mapping report.
        """

        rows = []

        for original, normalized, canonical in zip(
            report.original_columns,
            report.normalized_columns,
            report.canonical_columns,
        ):
            rows.append(
                {
                    "original": original,
                    "normalized": normalized,
                    "canonical": canonical,
                }
            )

        return pd.DataFrame(rows)


# ==========================================================
# Global Mapper
# ==========================================================

mapper = SchemaMapper()