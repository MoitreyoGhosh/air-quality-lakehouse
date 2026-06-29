"""
Master Lakehouse Pipeline
"""

from src.lakehouse.bronze import run as bronze

from src.lakehouse.silver import run as silver

from src.lakehouse.gold import run as gold

from src.database.views import create_views

from src.database.dataset_views import create_dataset_views


def main():

    print("=" * 80)
    print("ENVIRONMENTAL INTELLIGENCE LAKEHOUSE")
    print("=" * 80)

    # -------------------------------------------------

    print("\n[1/4] Bronze Layer\n")

    bronze()

    # -------------------------------------------------

    print("\n[2/4] Silver Layer\n")

    silver()

    # -------------------------------------------------

    print("\n[3/4] Gold Layer\n")

    gold()

    # -------------------------------------------------

    print("\n[4/4] Refresh DuckDB Views\n")

    # Refresh Metadata Views
    create_views()

    # Refresh Dataset Views
    create_dataset_views()

    # -------------------------------------------------

    print("\n")

    print("=" * 80)

    print("Pipeline Finished Successfully")

    print("=" * 80)


if __name__ == "__main__":

    main()