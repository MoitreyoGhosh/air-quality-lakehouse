"""
config.py
=====================================

DuckDB Configuration

Responsibilities
----------------
✓ Database file location
✓ Database schemas
✓ Global database constants

This module contains only configuration values.
"""

from __future__ import annotations

from pathlib import Path

from src.config import ROOT_DIR


# ==========================================================
# Database Location
# ==========================================================

DATABASE_DIR = ROOT_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_FILE = DATABASE_DIR / "air_quality_lakehouse.duckdb"


# ==========================================================
# Schema Names
# ==========================================================

BRONZE_SCHEMA = "bronze"

SILVER_SCHEMA = "silver"

GOLD_SCHEMA = "gold"

METADATA_SCHEMA = "metadata"


SCHEMAS = (
    BRONZE_SCHEMA,
    SILVER_SCHEMA,
    GOLD_SCHEMA,
    METADATA_SCHEMA,
)


# ==========================================================
# DuckDB Configuration
# ==========================================================

DUCKDB_CONFIG = {
    "threads": 4,
    "memory_limit": "4GB",
    "temp_directory": str(DATABASE_DIR / "temp"),
}


# ==========================================================
# Metadata Tables
# ==========================================================

DATASET_REGISTRY = "dataset_registry"

INGESTION_LOG = "ingestion_log"

VALIDATION_LOG = "validation_log"

PIPELINE_LOG = "pipeline_log"


# ==========================================================
# Helper Paths
# ==========================================================

TEMP_DIR = DATABASE_DIR / "temp"

EXPORT_DIR = DATABASE_DIR / "exports"

TEMP_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)