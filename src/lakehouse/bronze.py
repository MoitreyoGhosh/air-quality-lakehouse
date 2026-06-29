"""
Bronze Layer Pipeline

Copies raw source datasets into the Bronze layer
and registers metadata in DuckDB.
"""

from src.config import (
    RAW_DIR,
    BRONZE_DIR,
)

from src.lakehouse.manager import LakehouseManager


def run():
    manager = LakehouseManager(
        source_dir=RAW_DIR,
        target_dir=BRONZE_DIR,
        layer="bronze"
    )

    manager.ingest()

if __name__ == "__main__":
    run()