"""
bronze.py
--------------------------

Bronze Layer Pipeline

Responsibilities
----------------
1. Copy raw datasets to Bronze layer
2. Validate Bronze datasets
3. Register metadata
4. Log pipeline execution

The actual implementation is handled by:
    - LakehouseManager
    - DatasetValidator
"""

from pathlib import Path

from src.config import RAW_DIR, BRONZE_DIR
from src.lakehouse.manager import LakehouseManager
from src.lakehouse.validation import DatasetValidator


class BronzePipeline:

    def __init__(self):

        self.manager = LakehouseManager(
            source_dir=RAW_DIR,
            target_dir=BRONZE_DIR,
            layer="bronze"
        )

    def validate_bronze(self):
        """
        Validate every dataset copied into Bronze.
        """

        print("\n" + "=" * 70)
        print("BRONZE VALIDATION")
        print("=" * 70)

        validation_passed = True

        for dataset in BRONZE_DIR.rglob("*"):

            if dataset.suffix.lower() not in [
                ".xlsx",
                ".csv",
                ".parquet"
            ]:
                continue

            validator = DatasetValidator(dataset)

            report = validator.validate()

            validator.print_report(report)

            # Stop pipeline if any validation fails

            if (
                not report["file_exists"]
                or report["empty"]
                or report["duplicates"] > 0
            ):
                validation_passed = False

        return validation_passed

    def run(self):

        print("\n" + "=" * 80)
        print("BRONZE LAYER")
        print("=" * 80)

        # -------------------------------------------------
        # Step 1 : Ingestion
        # -------------------------------------------------

        self.manager.ingest()

        # -------------------------------------------------
        # Step 2 : Validation
        # -------------------------------------------------

        passed = self.validate_bronze()

        if passed:

            print("\n✅ Bronze Layer Validation PASSED")

        else:

            print("\n❌ Bronze Layer Validation FAILED")

            raise RuntimeError(
                "Bronze validation failed. Pipeline stopped."
            )

        return True


def run():

    BronzePipeline().run()


if __name__ == "__main__":

    run()