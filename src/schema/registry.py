"""
registry.py
=====================================

Schema Registry

The Schema Registry stores the canonical schemas discovered
from different datasets and provides utilities for
registration, retrieval, comparison and validation.

Responsibilities
----------------
✓ Register discovered schemas
✓ Retrieve schemas
✓ List registered datasets
✓ Compare schemas
✓ Find missing/extra columns
✓ Export schema metadata

This module NEVER modifies data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


# ==========================================================
# Schema Definition
# ==========================================================

@dataclass
class Schema:

    name: str

    raw_columns: List[str] = field(default_factory=list)

    normalized_columns: List[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)


# ==========================================================
# Schema Registry
# ==========================================================

class SchemaRegistry:
    """
    Runtime schema registry.
    """

    def __init__(self):

        self._schemas: Dict[str, Schema] = {}

    # ======================================================

    def register(
        self,
        name: str,
        raw_columns: List[str],
        normalized_columns: List[str],
        metadata: dict | None = None,
    ) -> None:
        """
        Register a discovered schema.
        """

        self._schemas[name] = Schema(
            name=name,
            raw_columns=list(raw_columns),
            normalized_columns=list(normalized_columns),
            metadata=metadata or {},
        )

    # ======================================================

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove a schema.
        """

        self._schemas.pop(name, None)

    # ======================================================

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check if schema exists.
        """

        return name in self._schemas

    # ======================================================

    def get(
        self,
        name: str,
    ) -> Schema:
        """
        Retrieve schema.
        """

        if name not in self._schemas:

            raise KeyError(
                f"Schema '{name}' is not registered."
            )

        return self._schemas[name]

    # ======================================================

    def available(self) -> list[str]:
        """
        Registered schema names.
        """

        return sorted(self._schemas.keys())

    # ======================================================

    def clear(self) -> None:
        """
        Remove all schemas.
        """

        self._schemas.clear()

    # ======================================================

    def compare(
        self,
        left: str,
        right: str,
    ) -> dict:
        """
        Compare two registered schemas.
        """

        schema_a = self.get(left)

        schema_b = self.get(right)

        left_columns = set(schema_a.normalized_columns)

        right_columns = set(schema_b.normalized_columns)

        return {

            "common":

                sorted(
                    left_columns &
                    right_columns
                ),

            "only_left":

                sorted(
                    left_columns -
                    right_columns
                ),

            "only_right":

                sorted(
                    right_columns -
                    left_columns
                ),
        }

    # ======================================================

    def validate(
        self,
        schema_name: str,
        dataframe_columns: List[str],
    ) -> dict:
        """
        Compare dataframe columns against
        a registered schema.
        """

        schema = self.get(schema_name)

        expected = set(
            schema.normalized_columns
        )

        received = set(
            dataframe_columns
        )

        return {

            "missing":

                sorted(
                    expected -
                    received
                ),

            "extra":

                sorted(
                    received -
                    expected
                ),

            "valid":

                expected == received,

        }

    # ======================================================

    def summary(self):
        """
        Registry summary.
        """

        rows = []

        for schema in self._schemas.values():

            rows.append({

                "schema":

                    schema.name,

                "columns":

                    len(
                        schema.normalized_columns
                    ),

                "raw_columns":

                    len(
                        schema.raw_columns
                    ),

            })

        try:

            import pandas as pd

            return pd.DataFrame(rows)

        except ImportError:

            return rows

    # ======================================================

    def export(self) -> dict:
        """
        Export registry as dictionary.
        """

        result = {}

        for schema in self._schemas.values():

            result[schema.name] = {

                "raw":

                    schema.raw_columns,

                "normalized":

                    schema.normalized_columns,

                "metadata":

                    schema.metadata,

            }

        return result


# ==========================================================
# Global Registry
# ==========================================================

registry = SchemaRegistry()