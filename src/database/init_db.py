from .connection import database
from .initializer import initializer
from .config import DATABASE_FILE


def initialize_database():
    database.connect()
    initializer.initialize()

    print("=" * 60)
    print("DuckDB Initialized Successfully")
    print("=" * 60)
    print(f"Database : {DATABASE_FILE}")

    database.close()


if __name__ == "__main__":
    initialize_database()