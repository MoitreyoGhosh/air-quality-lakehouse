from src.database.connection import get_connection

def create_schema():
    con = get_connection()
    con.execute("""

    CREATE TABLE IF NOT EXISTS datasets(
        dataset_name VARCHAR PRIMARY KEY,
        layer VARCHAR,
        source VARCHAR,
        format VARCHAR,
        rows BIGINT,
        columns INTEGER,
        version VARCHAR,
        checksum VARCHAR,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );

    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS files(
        file_name VARCHAR PRIMARY KEY,
        dataset_name VARCHAR,
        layer VARCHAR,
        file_path VARCHAR,
        file_size_mb DOUBLE,
        created_at TIMESTAMP
    );

    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_runs(
        run_id BIGINT,
        pipeline_name VARCHAR,
        layer VARCHAR,
        status VARCHAR,
        started_at TIMESTAMP,
        finished_at TIMESTAMP,
        message VARCHAR
    );

    """)

    con.close()

if __name__ == "__main__":
    create_schema()
    print("Schema Created Successfully")