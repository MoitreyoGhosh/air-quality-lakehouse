"""
Bronze Layer Pipeline

Copies raw source datasets into the Bronze layer
and registers metadata in DuckDB.
"""

# from src.config import (
#     RAW_DIR,
#     BRONZE_DIR,
# )

# from src.lakehouse.manager import LakehouseManager


# def run():
#     manager = LakehouseManager(
#         source_dir=RAW_DIR,
#         target_dir=BRONZE_DIR,
#         layer="bronze"
#     )

#     manager.ingest()

# if __name__ == "__main__":
#     run()

from pathlib import Path

from src.config import RAW_DIR, BRONZE_DIR

from src.lakehouse.manager import LakehouseManager

from src.lakehouse.validation import DatasetValidator


def run():

    print("\nStarting Bronze Pipeline...\n")

    manager = LakehouseManager(

        RAW_DIR,

        BRONZE_DIR,

        "bronze"

    )

    manager.ingest()

    print("\nValidating Bronze Layer...\n")

    for dataset in BRONZE_DIR.rglob("*"):

        if dataset.suffix in [".parquet", ".xlsx", ".csv"]:

            validator = DatasetValidator(dataset)

            report = validator.validate()

            validator.print_report(report)

    print("\nBronze Pipeline Completed.\n")


if __name__ == "__main__":

    run()