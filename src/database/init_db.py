from src.database.connection import get_connection
from src.config import DUCKDB_PATH


def initialize_database():

    connection = get_connection()

    print("=" * 60)
    print("DuckDB Initialized Successfully")
    print("=" * 60)
    print(f"Database : {DUCKDB_PATH}")

    connection.close()


if __name__ == "__main__":

    initialize_database()