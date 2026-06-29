"""
Creates all metadata tables required by the
Environmental Intelligence Lakehouse.
"""

from src.database.connection import get_connection

def create_schema():
    con = get_connection()

    # DATASETS
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

    # FILES
    con.execute("""
    CREATE TABLE IF NOT EXISTS files(
        file_name VARCHAR PRIMARY KEY,
        dataset_name VARCHAR,
        layer VARCHAR,
        file_path VARCHAR,
        file_size_mb DOUBLE,
        created_at TIMESTAMP,
        FOREIGN KEY(dataset_name)
        REFERENCES datasets(dataset_name)
    );
    """)

    # PIPELINE RUNS
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

    # VALIDATION RESULTS
    con.execute("""
    CREATE TABLE IF NOT EXISTS validation_results(
        validation_id BIGINT,
        dataset_name VARCHAR,
        layer VARCHAR,
        check_name VARCHAR,
        status VARCHAR,
        value VARCHAR,
        checked_at TIMESTAMP,
        FOREIGN KEY(dataset_name)
        REFERENCES datasets(dataset_name)
    );
    """)

    # DATASET VERSIONS
    con.execute("""
    CREATE TABLE IF NOT EXISTS dataset_versions(
        version_id BIGINT,
        dataset_name VARCHAR,
        version VARCHAR,
        checksum VARCHAR,
        created_at TIMESTAMP,
        FOREIGN KEY(dataset_name)
        REFERENCES datasets(dataset_name)
    );
    """)

    # DATASET STATISTICS
    con.execute("""
    CREATE TABLE IF NOT EXISTS dataset_statistics(
        dataset_name VARCHAR PRIMARY KEY,
        row_count BIGINT,
        column_count INTEGER,
        null_count BIGINT,
        duplicate_count BIGINT,
        last_updated TIMESTAMP,
        FOREIGN KEY(dataset_name)
        REFERENCES datasets(dataset_name)
    );
    """)

    con.close()

if __name__ == "__main__":

    create_schema()

    print("=" * 60)
    print("Lakehouse Schema Created Successfully")
    print("=" * 60)