from src.database.connection import get_connection

con = get_connection()

tables = [
    "datasets",
    "files",
    "pipeline_runs",
    "validation_results",
    "dataset_versions",
    "dataset_statistics"
]

for table in tables:

    print("\n" + "=" * 70)
    print(table.upper())
    print("=" * 70)

    print(
        con.execute(f"DESCRIBE {table};").fetchdf()
    )

con.close()