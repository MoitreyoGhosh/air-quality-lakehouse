"""
initializer.py
=====================================

Database Initializer

Creates the required Lakehouse schemas.

Responsibilities
----------------
✓ Initialize database schemas
✓ Reset database (development)
"""

from __future__ import annotations

from .config import SCHEMAS
from .connection import database


class DatabaseInitializer:
    """
    Initialize the DuckDB database.
    """

    def initialize(self) -> None:
        """
        Create all required schemas.
        """

        conn = database.connection

        for schema in SCHEMAS:
            conn.execute(
                f"CREATE SCHEMA IF NOT EXISTS {schema};"
            )

    def reset(self) -> None:
        """
        Drop and recreate all schemas.
        """

        conn = database.connection

        for schema in reversed(SCHEMAS):
            conn.execute(
                f"DROP SCHEMA IF EXISTS {schema} CASCADE;"
            )

        self.initialize()


initializer = DatabaseInitializer()