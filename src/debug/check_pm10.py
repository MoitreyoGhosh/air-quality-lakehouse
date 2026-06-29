import duckdb

con = duckdb.connect()

print(
    con.execute("""
    SELECT
        MIN(pm10),
        MAX(pm10)
    FROM read_parquet('lakehouse/silver/wbpcb_master.parquet')
    """).fetchall()
)

print()

print(
    con.execute("""
    SELECT *
    FROM read_parquet('lakehouse/silver/wbpcb_master.parquet')
    WHERE pm10 < 0
    LIMIT 20
    """).fetchdf()
)