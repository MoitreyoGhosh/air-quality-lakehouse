"""
utils.py
=====================================

DuckDB Utility Functions

Responsibilities
----------------
✓ Execute SQL
✓ Register DataFrames
✓ Check table existence
✓ List schemas and tables

This module provides reusable helpers for the
database layer.
"""

from __future__ import annotations

import pandas as pd

from .connection import database


class DatabaseUtils:
    """
    Helper utilities for DuckDB operations.
    """

    # =====================================================
    # Execute SQL
    # =====================================================

    @staticmethod
    def execute(sql: str):
        """
        Execute an SQL statement.
        """

        conn = database.connection
        return conn.execute(sql)

    # =====================================================
    # Query
    # =====================================================

    @staticmethod
    def query(sql: str) -> pd.DataFrame:
        """
        Execute a query and return a DataFrame.
        """

        conn = database.connection
        return conn.execute(sql).df()

    # =====================================================
    # Register DataFrame
    # =====================================================

    @staticmethod
    def register(name: str, df: pd.DataFrame) -> None:
        """
        Register a pandas DataFrame as a temporary DuckDB view.
        """

        conn = database.connection
        conn.register(name, df)

    # =====================================================
    # Unregister
    # =====================================================

    @staticmethod
    def unregister(name: str) -> None:
        """
        Remove a registered view.
        """

        conn = database.connection
        conn.unregister(name)

    # =====================================================
    # Table Exists
    # =====================================================

    @staticmethod
    def table_exists(
        schema: str,
        table: str,
    ) -> bool:
        """
        Check whether a table exists.
        """

        sql = f"""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema='{schema}'
          AND table_name='{table}'
        """

        return bool(
            DatabaseUtils.execute(sql).fetchone()[0]
        )

    # =====================================================
    # List Tables
    # =====================================================

    @staticmethod
    def list_tables(
        schema: str,
    ) -> list[str]:
        """
        List all tables in a schema.
        """

        sql = f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='{schema}'
        ORDER BY table_name
        """

        return (
            DatabaseUtils.query(sql)
            .table_name
            .tolist()
        )

    # =====================================================
    # Row Count
    # =====================================================

    @staticmethod
    def row_count(
        schema: str,
        table: str,
    ) -> int:
        """
        Return row count for a table.
        """

        sql = f"""
        SELECT COUNT(*)
        FROM {schema}.{table}
        """

        return DatabaseUtils.execute(sql).fetchone()[0]