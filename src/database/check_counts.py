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

print("=" * 70)
print("ROW COUNTS")
print("=" * 70)

for table in tables:

    count = con.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table:<25} : {count}")

con.close()