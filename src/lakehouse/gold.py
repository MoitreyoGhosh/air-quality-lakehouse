"""
Gold Layer Pipeline
"""

from src.config import CURATED_DIR, GOLD_DIR
from src.lakehouse.manager import LakehouseManager
from src.lakehouse.validation import DatasetValidator


class GoldPipeline:

    def __init__(self):
        self.manager = LakehouseManager(
            source_dir=CURATED_DIR,
            target_dir=GOLD_DIR,
            layer="gold"
        )

    def validate_gold(self):
        print("\n" + "=" * 70)
        print("GOLD VALIDATION")
        print("=" * 70)

        validation_passed = True

        for dataset in GOLD_DIR.rglob("*"):

            if dataset.suffix.lower() not in [
                ".parquet",
                ".csv",
                ".xlsx"
            ]:
                continue

            validator = DatasetValidator(
                dataset_path=dataset,
                layer="gold"
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
        print("GOLD LAYER")
        print("=" * 80)

        self.manager.ingest()
        passed = self.validate_gold()

# BYPASSING GOLD LAYER VALIDATION FOR NOW
        if passed:
            print("\n✅ Gold Layer Validation PASSED")
        else:
            print("\n❌ Gold Layer Validation FAILED")

def run():
    GoldPipeline().run()


if __name__ == "__main__":
    run()