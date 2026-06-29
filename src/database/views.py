"""
views.py

Creates analytical metadata views for the Data Lakehouse.
"""

from src.database.connection import get_connection


def create_views():

    con = get_connection()

    # ==========================================================
    # Dataset Catalog
    # ==========================================================

    con.execute("""
    CREATE OR REPLACE VIEW dataset_catalog AS

    SELECT

        dataset_name,

        layer,

        source,

        format,

        rows,

        columns,

        version,

        updated_at

    FROM datasets

    ORDER BY
        layer,
        dataset_name;
    """)

    # ==========================================================
    # Pipeline History
    # ==========================================================

    con.execute("""
    CREATE OR REPLACE VIEW pipeline_history AS

    SELECT

        run_id,

        pipeline_name,

        layer,

        status,

        started_at,

        finished_at,

        message

    FROM pipeline_runs

    ORDER BY
        run_id DESC;
    """)

    # ==========================================================
    # Layer Summary
    # ==========================================================

    con.execute("""
    CREATE OR REPLACE VIEW layer_summary AS

    SELECT

        d.layer,

        COUNT(*) AS total_datasets,

        SUM(rows) AS total_rows,

        SUM(file_size_mb) AS total_size_mb

    FROM

        datasets d

    JOIN

        files f

    ON

        d.dataset_name = f.dataset_name

    GROUP BY

        d.layer

    ORDER BY

        d.layer;
    """)

    # ==========================================================
    # File Catalog
    # ==========================================================

    con.execute("""
    CREATE OR REPLACE VIEW file_catalog AS

    SELECT

        file_name,

        dataset_name,

        layer,

        file_path,

        ROUND(file_size_mb,2) AS size_mb,

        created_at

    FROM files

    ORDER BY

        layer,
        file_name;
    """)

    con.close()

    print("=" * 60)
    print("Metadata Views Created Successfully")
    print("=" * 60)


if __name__ == "__main__":
    create_views()