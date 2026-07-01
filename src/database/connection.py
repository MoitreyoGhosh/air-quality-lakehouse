"""
connection.py
=====================================

DuckDB Connection Manager

Responsibilities
----------------
✓ Open DuckDB connection
✓ Apply database configuration
✓ Close connection

This module contains no schema or table creation logic.
"""

from __future__ import annotations

import duckdb

from .config import DATABASE_FILE, DUCKDB_CONFIG


class DatabaseConnection:
    """
    Manage the application's DuckDB connection.
    """

    def __init__(self):
        self._connection: duckdb.DuckDBPyConnection | None = None

    # ======================================================
    # Connection
    # ======================================================

    def connect(self) -> duckdb.DuckDBPyConnection:
        """
        Create or return an active DuckDB connection.
        """

        if self._connection is None:
            self._connection = duckdb.connect(str(DATABASE_FILE))
            self._configure()

        return self._connection

    # ======================================================
    # Configuration
    # ======================================================

    def _configure(self) -> None:
        """
        Apply DuckDB runtime settings.
        """

        if self._connection is None:
            return

        for key, value in DUCKDB_CONFIG.items():
            self._connection.execute(
                f"SET {key}='{value}'"
            )

    # ======================================================
    # Access
    # ======================================================

    @property
    def connection(self) -> duckdb.DuckDBPyConnection:
        """
        Return an active connection.
        """

        return self.connect()

    # ======================================================
    # Close
    # ======================================================

    def close(self) -> None:
        """
        Close the database connection.
        """

        if self._connection is not None:
            self._connection.close()
            self._connection = None


# ==========================================================
# Singleton
# ==========================================================

database = DatabaseConnection()