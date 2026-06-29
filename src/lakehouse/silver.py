"""
Silver Layer Pipeline

Copies processed datasets into the Silver layer
and registers metadata in DuckDB.
"""

from src.config import (
    PROCESSED_DIR,
    SILVER_DIR,
)

from src.lakehouse.manager import LakehouseManager

def run():
    manager = LakehouseManager(
        source_dir=PROCESSED_DIR,
        target_dir=SILVER_DIR,
        layer="silver"
    )

    manager.ingest()

if __name__ == "__main__":
    run()