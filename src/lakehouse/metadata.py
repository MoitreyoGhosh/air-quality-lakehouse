"""
Utility functions for managing the Lakehouse metadata catalog.
"""

from pathlib import Path
from datetime import datetime
import hashlib

from src.database.connection import get_connection

# Utility Functions
def calculate_checksum(file_path: Path) -> str:
    """
    Calculate SHA256 checksum for a file.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()

# Dataset Registration
def register_dataset(
    dataset_name: str,
    layer: str,
    source: str,
    file_format: str,
    rows: int,
    columns: int,
    version: str,
    checksum: str
):
    """
    Register or update a dataset in DuckDB.
    """

    con = get_connection()

    con.execute(
        """
        INSERT OR REPLACE INTO datasets
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            dataset_name,
            layer,
            source,
            file_format,
            rows,
            columns,
            version,
            checksum,
            datetime.now(),
            datetime.now()
        )
    )

    con.close()

# File Registration
def register_file(
    file_name: str,
    dataset_name: str,
    layer: str,
    file_path: str,
    file_size_mb: float
):
    """
    Register a physical file.
    """

    con = get_connection()

    con.execute(
        """
        INSERT OR REPLACE INTO files
        VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
        """,
        (
            file_name,
            dataset_name,
            layer,
            file_path,
            file_size_mb,
            datetime.now()
        )
    )

    con.close()

# Pipeline Logging
def log_pipeline(
    pipeline_name: str,
    layer: str,
    status: str,
    message: str
):
    """
    Record every pipeline execution.
    """

    con = get_connection()

    run_id = con.execute(
        """
        SELECT COALESCE(MAX(run_id), 0) + 1
        FROM pipeline_runs
        """
    ).fetchone()[0]

    now = datetime.now()

    con.execute(
        """
        INSERT INTO pipeline_runs
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            run_id,
            pipeline_name,
            layer,
            status,
            now,
            now,
            message
        )
    )

    con.close()

# Metadata Queries
def list_datasets():
    con = get_connection()

    df = con.execute(
        """
        SELECT *
        FROM datasets
        ORDER BY dataset_name
        """
    ).fetchdf()

    con.close()

    return df


def list_pipeline_runs():
    con = get_connection()

    df = con.execute(
        """
        SELECT *
        FROM pipeline_runs
        ORDER BY run_id DESC
        """
    ).fetchdf()

    con.close()

    return df


def list_files():
    con = get_connection()

    df = con.execute(
        """
        SELECT *
        FROM files
        ORDER BY file_name
        """
    ).fetchdf()
    con.close()

    return df