"""
bronze.py
=====================================

Bronze Lakehouse Layer

Responsibilities
----------------
✓ Persist validated canonical datasets
✓ Create Bronze tables dynamically
✓ Preserve raw records (no cleaning)
✓ Register datasets in metadata
✓ Log ingestion events

The Bronze layer is immutable and stores the
canonical representation of the source data.
"""

from __future__ import annotations

from typing import Dict
from pathlib import Path
import pandas as pd

from src.database.connection import database
from src.database.utils import DatabaseUtils
from src.lakehouse.metadata import metadata


class BronzeLayer:
    """
    Bronze Lakehouse Manager.
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        self.connection = database.connection

        self.project_root = Path.cwd()

        self.bronze_directory = (
            self.project_root
            / "data"
            / "bronze"
        )

        self.bronze_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def initialize(self) -> None:
        """
        Initialize metadata tables.
        """

        metadata.initialize()

    # =====================================================
    # Table Name
    # =====================================================

    @staticmethod
    def table_name(dataset_name: str) -> str:
        """
        Convert dataset name into a DuckDB-safe table name.
        """

        return (
            dataset_name.lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace(",", "")
            .replace(".", "")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
        )

    # =====================================================
    # Write Dataset
    # =====================================================

    def write(
        self,
        dataset_name: str,
        df: pd.DataFrame,
        source: str,
    ) -> None:
        """
        Persist a single dataset into Bronze.
        """

        
        conn = database.connection

        table = self.table_name(dataset_name)

        # -------------------------------------------------
        # Preserve source lineage
        # -------------------------------------------------

        df = df.copy()

        df["source_dataset"] = dataset_name      # Original dataset/file name
        df["source"] = source                    # WBPCB / OPENMETEO
        df["bronze_table"] = table               # DuckDB table name

    
        # Register dataframe temporarily
        DatabaseUtils.register(
            "dataset_df",
            df,
        )

        # Replace table with latest version
        conn.execute(
            f"""
            CREATE OR REPLACE TABLE bronze.{table} AS
            SELECT *
            FROM dataset_df;
            """
        )

        DatabaseUtils.unregister(
            "dataset_df"
        )
        
        # -------------------------------------------------
        # Save Parquet
        # -------------------------------------------------
        
        self.save_parquet(
            table,
            df,
        )
        
        # -------------------------------------------------
        # Register metadata
        # -------------------------------------------------
        
        metadata.register_dataset(
            dataset_name=dataset_name,
            source=source,
            layer="bronze",
            rows=len(df),
            columns=len(df.columns),
        )
        
        metadata.log_ingestion(
            dataset_name=dataset_name,
            source=source,
            layer="bronze",
            status="SUCCESS",
            rows=len(df),
        )
    
    # =====================================================
    # Save Parquet
    # =====================================================
    
    def save_parquet(
        self,
        table: str,
        df: pd.DataFrame,
    ) -> None:
    
        path = (
            self.bronze_directory
            / f"{table}.parquet"
        )
    
        df.to_parquet(
            path,
            index=False,
        )
    
        assert path.exists(), (
            f"Failed to export {path}"
        )
    
        print(
            f"✓ Saved {path.name}"
        )
    
    # =====================================================
    # Batch Write
    # =====================================================

    def write_all(
        self,
        datasets: Dict[str, pd.DataFrame],
        source: str,
    ) -> None:
        """
        Persist multiple datasets.
        """

        self.initialize()

        for dataset_name, df in datasets.items():
            self.write(
                dataset_name=dataset_name,
                df=df,
                source=source,
            )

    # =====================================================
    # Read Dataset
    # =====================================================

    def read(
        self,
        dataset_name: str,
    ) -> pd.DataFrame:
        """
        Read a Bronze dataset.
        """

        table = self.table_name(dataset_name)

        return DatabaseUtils.query(
            f"""
            SELECT *
            FROM bronze.{table}
            """
        )

    # =====================================================
    # List Tables
    # =====================================================

    @staticmethod
    def tables() -> list[str]:
        """
        List all Bronze tables.
        """

        return DatabaseUtils.list_tables("bronze")

    # =====================================================
    # Summary
    # =====================================================

    @staticmethod
    def summary() -> pd.DataFrame:
        """
        Return Bronze dataset registry.
        """

        return metadata.dataset_registry()


# ==========================================================
# Singleton
# ==========================================================

bronze = BronzeLayer()