import duckdb

from src.config import DUCKDB_PATH

def get_connection():
    return duckdb.connect(DUCKDB_PATH)