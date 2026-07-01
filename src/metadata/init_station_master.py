from pathlib import Path

import pandas as pd

from src.database.connection import database
from src.database.utils import DatabaseUtils


def initialize_station_master():

    csv_path = Path("data/metadata/station_master.csv")

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Station metadata not found: {csv_path.resolve()}"
        )

    df = pd.read_csv(csv_path)

    print(f"Loaded {len(df)} stations from {csv_path}")

    DatabaseUtils.register(
        "station_master_df",
        df,
    )

    # Create schema if required
    database.connection.execute(
        """
        CREATE SCHEMA IF NOT EXISTS metadata;
        """
    )

    # Create table
    database.connection.execute(
        """
        CREATE OR REPLACE TABLE metadata.station_master AS
        SELECT *
        FROM station_master_df;
        """
    )

    DatabaseUtils.unregister(
        "station_master_df"
    )

    print("metadata.station_master initialized successfully.")
    print(df.head())


if __name__ == "__main__":
    initialize_station_master()