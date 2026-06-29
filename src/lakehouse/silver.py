"""
Silver Layer Pipeline
"""

from src.config import PROCESSED_DIR, SILVER_DIR
from src.lakehouse.manager import LakehouseManager
from src.lakehouse.validation import DatasetValidator


class SilverPipeline:

    def __init__(self):
        self.manager = LakehouseManager(
            source_dir=PROCESSED_DIR,
            target_dir=SILVER_DIR,
            layer="silver"
        )

    def validate_silver(self):
        print("\n" + "=" * 70)
        print("SILVER VALIDATION")
        print("=" * 70)

        validation_passed = True
        for dataset in SILVER_DIR.rglob("*"):

            if dataset.suffix.lower() not in [
                ".parquet",
                ".csv",
                ".xlsx"
            ]:
                continue

            validator = DatasetValidator(
                dataset_path=dataset,
                layer="silver"
            )

            report = validator.validate()
            validator.print_report(report)

            if (
                not report["file_exists"]
                or report["empty"]
                or report["duplicates"] > 0
            ):
                validation_passed = False

        return validation_passed

    def run(self):

        print("\n" + "=" * 80)
        print("SILVER LAYER")
        print("=" * 80)

        self.manager.ingest()

        passed = self.validate_silver()

# BYPASSING SILVER LAYER VALIDATION FOR NOW
        if passed:
            print("\n✅ Silver Layer Validation PASSED")
        else:
            print("\n❌ Silver Layer Validation FAILED")


def run():
    SilverPipeline().run()


if __name__ == "__main__":
    run()