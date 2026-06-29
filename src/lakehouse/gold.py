"""
Gold Layer Pipeline

Copies curated datasets into the Gold layer
and registers metadata in DuckDB.
"""

from src.config import (
    CURATED_DIR,
    GOLD_DIR,
)

from src.lakehouse.manager import LakehouseManager


def run():
    manager = LakehouseManager(
        source_dir=CURATED_DIR,
        target_dir=GOLD_DIR,
        layer="gold"
    )

    manager.ingest()

if __name__ == "__main__":
    run()