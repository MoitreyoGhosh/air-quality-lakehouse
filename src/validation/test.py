"""
test.py
=====================================

Validation Pipeline Test

Tests the complete validation workflow:

Historical Ingestion
        │
        ▼
Canonical DataFrames
        │
        ▼
Data Validator
        │
        ▼
Validation Report
"""

from src.config import RAW_DIR
from src.ingestion.historical import HistoricalIngestion
from src.validation.validator import DataValidator
from src.validation.report import ValidationReport


def test_dataset(
    connector_name: str,
    source,
    dataset_type: str,
) -> None:
    """
    Test validation pipeline for a connector.
    """

    ingestion = HistoricalIngestion()
    validator = DataValidator()

    datasets = ingestion.ingest(
        connector_name=connector_name,
        source=source,
    )

    print("\n")
    print("=" * 80)
    print(f"{connector_name.upper()} VALIDATION")
    print("=" * 80)

    print("\nIngestion Summary")
    print("-" * 80)
    print(ingestion.summary(datasets))

    for dataset_name, df in datasets.items():

        result = validator.validate(
            df=df,
            dataset_type=dataset_type,
        )

        ValidationReport.print_report(
            dataset_name,
            result,
        )

        # Validate one dataset at a time
        break


if __name__ == "__main__":

    # =====================================================
    # WBPCB
    # =====================================================

    test_dataset(
        connector_name="wbpcb",
        source=RAW_DIR,
        dataset_type="wbpcb",
    )

    # =====================================================
    # Open-Meteo
    # =====================================================

    test_dataset(
        connector_name="openmeteo",
        source=RAW_DIR / "open-meteo-weather",
        dataset_type="openmeteo",
    )