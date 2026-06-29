import duckdb

con = duckdb.connect()

print(
    con.execute("""
    SELECT
        MIN(aqi),
        MAX(aqi)
    FROM read_parquet('lakehouse/silver/wbpcb_master.parquet')
    """).fetchall()
)

print()

print(
    con.execute("""
    SELECT *
    FROM read_parquet('lakehouse/silver/wbpcb_master.parquet')
    WHERE aqi < 0
       OR aqi > 500
    LIMIT 20
    """).fetchdf()
)