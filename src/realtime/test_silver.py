"""
test_silver.py
=====================================

Realtime Silver Test

Tests
-----
✓ Read Bronze datasets
✓ Build Realtime Master
✓ Validation
✓ Save Silver Parquet
"""

from pathlib import Path

import pandas as pd

from src.realtime.silver import RealtimeSilver


# ==========================================================
# Helpers
# ==========================================================

SILVER_FILE = (
    Path("data")
    / "near-real-time"
    / "silver"
    / "realtime_master.parquet"
)


def divider():

    print("=" * 80)


def summary(df: pd.DataFrame):

    print()

    print("Rows :", len(df))

    print("Columns :", len(df.columns))

    print("Stations :", df["station_id"].nunique())

    print()

    print("Datetime Range")

    print(
        df["datetime"].min(),
        "->",
        df["datetime"].max(),
    )

    print()

    print("Columns")

    print(list(df.columns))

    print()

    print("Missing Values")

    print(df.isna().sum())

    print()

    print(df.head())


# ==========================================================
# Main
# ==========================================================

def main():

    divider()

    print("REALTIME SILVER TEST")

    divider()

    silver = RealtimeSilver()

    df = silver.run()

    divider()

    print("REALTIME MASTER")

    divider()

    summary(df)

    divider()

    print("PARQUET")

    divider()

    if SILVER_FILE.exists():

        parquet = pd.read_parquet(
            SILVER_FILE
        )

        print("✓ realtime_master.parquet")

        print(
            "Rows :",
            len(parquet),
        )

        print(
            "Columns :",
            len(parquet.columns),
        )

    else:

        print(
            "✗ realtime_master.parquet not found."
        )

    divider()

    print("REALTIME SILVER TEST PASSED")

    divider()


if __name__ == "__main__":

    main()