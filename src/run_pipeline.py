"""
pipeline.py
=====================================

Master Lakehouse Pipeline

Workflow
--------
Historical Ingestion
        ↓
Validation
        ↓
Bronze
        ↓
Silver
        ↓
Gold
        ↓
DuckDB Views
"""

from src.ingestion.historical import HistoricalIngestion
from src.validation.validator import DataValidator

from src.lakehouse.bronze import bronze
from src.metadata.init_station_master import initialize_station_master
from src.lakehouse.silver import SilverLayer
# from src.lakehouse.gold import gold

# from src.database.views import create_views
# from src.database.dataset_views import create_dataset_views


def main():

    print("=" * 80)
    print("ENVIRONMENTAL INTELLIGENCE LAKEHOUSE")
    print("=" * 80)

    # =====================================================
    # 1. Historical Ingestion
    # =====================================================

    print("\n[1/7] Historical Ingestion\n")

    ingestion = HistoricalIngestion()

    wbpcb_datasets = ingestion.ingest(
        connector_name="WBPCB",
        source="data/raw/wbpcb/",
    )

    openmeteo_datasets = ingestion.ingest(
        connector_name="OPENMETEO",
        source="data/raw/open-meteo-weather/",
    )

    print("\nIngested Datasets:")
    print(f"  - WBPCB: {len(wbpcb_datasets)} datasets")
    print(f"  - OPENMETEO: {len(openmeteo_datasets)} datasets")

    # =====================================================
    # 2. Validation
    # =====================================================

    print("\n[2/7] Validation\n")
    
    
    validator = DataValidator()
    wbpcb_datasets = validator.validate_all(
        wbpcb_datasets,
        dataset_type="WBPCB",
    )
    openmeteo_datasets = validator.validate_all(
        openmeteo_datasets,
        dataset_type="OPENMETEO",
    )

    print("\nValidation Complete")

    # =====================================================
    # 3. Bronze Layer
    # =====================================================

    print("\n[3/7] Bronze Layer\n")

    bronze.write_all(
        wbpcb_datasets,
        source="WBPCB",
    )

    bronze.write_all(
        openmeteo_datasets,
        source="OPENMETEO",
    )

    print("\nBronze Layer Complete")
    print(f"  - WBPCB: {len(wbpcb_datasets)} datasets")
    print(f"  - OPENMETEO: {len(openmeteo_datasets)} datasets")

    initialize_station_master()

    # =====================================================
    # 4. Silver Layer
    # =====================================================

    print("\n[4/7] Silver Layer\n")

    silver_layer = SilverLayer()
    silver_summary = silver_layer.run()

    print(silver_summary)

    # ======================================================
    # 5. Silver Validation
    # ======================================================

    print("\n[5/7] Silver Validation")

    from src.lakehouse.silver_validation import (
        silver_validator,
    )

    validation_summary = silver_validator.run()

    print(validation_summary)
    # =====================================================
    # 6. Gold Layer
    # =====================================================

    print("\n[6/7] Gold Layer\n")

    #gold.run()

    # =====================================================
    # 7. Refresh Views
    # =====================================================

    print("\n[7/7] Refresh DuckDB Views\n")

    #create_views()
    #create_dataset_views()

    print("\n")
    print("=" * 80)
    print("Pipeline Finished Successfully")
    print("=" * 80)


if __name__ == "__main__":

    main()