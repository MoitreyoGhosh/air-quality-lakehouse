"""
metadata.py
=====================================

Lakehouse Metadata Manager

Responsibilities
----------------
✓ Create metadata tables
✓ Register datasets
✓ Log ingestion events
✓ Store validation summaries

This module never stores environmental data.
Only metadata about the lakehouse.
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from src.database import DatabaseUtils
from src.database.connection import database


class MetadataManager:
    """
    Manage metadata tables for the lakehouse.
    """
    # =====================================================
    # Initialization
    # =====================================================

    def initialize(self) -> None:
        """
        Create metadata tables if they do not exist.
        """
        conn = database.connection

        # ---------------------------------------------
        # Dataset Registry
        # ---------------------------------------------

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata.dataset_registry (
                dataset_name TEXT PRIMARY KEY,
                source TEXT,
                layer TEXT,
                rows INTEGER,
                columns INTEGER,
                created_at TIMESTAMP
            );
            """
        )

        # ---------------------------------------------
        # Ingestion Log
        # ---------------------------------------------

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata.ingestion_log (
                id BIGINT,
                dataset_name TEXT,
                source TEXT,
                layer TEXT,
                status TEXT,
                rows INTEGER,
                timestamp TIMESTAMP

            );
            """
        )

        # ---------------------------------------------
        # Validation Log
        # ---------------------------------------------

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata.validation_log (
                id BIGINT,
                dataset_name TEXT,
                duplicates INTEGER,
                missing_columns INTEGER,
                validation_time TIMESTAMP

            );
            """
        )

        #---------------------------------------------
        # Cleaning Report
        #---------------------------------------------
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata.cleaning_report (
            source TEXT,
            station TEXT,
            original_rows INTEGER,
            final_rows INTEGER,
            duplicates_removed INTEGER,
            empty_columns_removed INTEGER,
            invalid_timestamps INTEGER
            );
            """
        )

    # =====================================================
    # Dataset Registry
    # =====================================================

    def register_dataset(
        self,
        dataset_name: str,
        source: str,
        layer: str,
        rows: int,
        columns: int,
    ) -> None:
        """
        Register or update a dataset.
        """

        conn = database.connection

        conn.execute(
            """
            INSERT OR REPLACE INTO metadata.dataset_registry
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                dataset_name,
                source,
                layer,
                rows,
                columns,
                datetime.now(),
            ],
        )

    # =====================================================
    # Ingestion Log
    # =====================================================

    def log_ingestion(
        self,
        dataset_name: str,
        source: str,
        layer: str,
        status: str,
        rows: int,
    ) -> None:
        """
        Record an ingestion event.
        """

        conn = database.connection

        next_id = conn.execute(
            """
            SELECT COALESCE(MAX(id),0)+1
            FROM metadata.ingestion_log
            """
        ).fetchone()[0]

        conn.execute(
            """
            INSERT INTO metadata.ingestion_log
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                next_id,
                dataset_name,
                source,
                layer,
                status,
                rows,
                datetime.now(),
            ],
        )

    # =====================================================
    # Validation Log
    # =====================================================

    def log_validation(
        self,
        dataset_name: str,
        duplicates: int,
        missing_columns: int,
    ) -> None:
        """
        Store validation summary.
        """

        conn = database.connection

        next_id = conn.execute(
            """
            SELECT COALESCE(MAX(id),0)+1
            FROM metadata.validation_log
            """
        ).fetchone()[0]

        conn.execute(
            """
            INSERT INTO metadata.validation_log
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                next_id,
                dataset_name,
                duplicates,
                missing_columns,
                datetime.now(),
            ],
        )

    # =====================================================
    # Reports
    # =====================================================

    @staticmethod
    def dataset_registry() -> pd.DataFrame:
        """
        Return registered datasets.
        """

        return DatabaseUtils.query(
            """
            SELECT *
            FROM metadata.dataset_registry
            ORDER BY dataset_name
            """
        )

    @staticmethod
    def ingestion_history() -> pd.DataFrame:
        """
        Return ingestion history.
        """

        return DatabaseUtils.query(
            """
            SELECT *
            FROM metadata.ingestion_log
            ORDER BY timestamp DESC
            """
        )

    @staticmethod
    def validation_history() -> pd.DataFrame:
        """
        Return validation history.
        """

        return DatabaseUtils.query(
            """
            SELECT *
            FROM metadata.validation_log
            ORDER BY validation_time DESC
            """
        )


# ==========================================================
# Singleton
# ==========================================================

metadata = MetadataManager()