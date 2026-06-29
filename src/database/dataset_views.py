"""
dataset_views.py

Creates DuckDB SQL views over Lakehouse datasets.
"""

from src.database.connection import get_connection
from src.config import (
    GOLD_DIR,
    SILVER_DIR
)


def create_dataset_views():

    con = get_connection()

    # =====================================================
    # Gold Dataset Views
    # =====================================================

    con.execute(f"""
    CREATE OR REPLACE VIEW environmental_master AS

    SELECT *

    FROM read_parquet(
        '{GOLD_DIR / "environmental_master.parquet"}'
    );
    """)

    con.execute(f"""
    CREATE OR REPLACE VIEW realtime_environmental_master AS

    SELECT *

    FROM read_parquet(
        '{GOLD_DIR / "realtime_environmental_master.parquet"}'
    );
    """)

    # =====================================================
    # Silver Dataset Views
    # =====================================================

    con.execute(f"""
    CREATE OR REPLACE VIEW wbpcb_master AS

    SELECT *

    FROM read_parquet(
        '{SILVER_DIR / "wbpcb_master.parquet"}'
    );
    """)

    con.execute(f"""
    CREATE OR REPLACE VIEW weather_master AS

    SELECT *

    FROM read_parquet(
        '{SILVER_DIR / "openmeteo_weather_master.parquet"}'
    );
    """)

    con.execute(f"""
    CREATE OR REPLACE VIEW realtime_weather AS

    SELECT *

    FROM read_parquet(
        '{SILVER_DIR / "realtime_weather.parquet"}'
    );
    """)

    con.execute(f"""
    CREATE OR REPLACE VIEW realtime_aqi AS

    SELECT *

    FROM read_parquet(
        '{SILVER_DIR / "realtime_aqi.parquet"}'
    );
    """)

    con.close()

    print("=" * 60)
    print("Dataset Views Created Successfully")
    print("=" * 60)


if __name__ == "__main__":
    create_dataset_views()