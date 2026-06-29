import duckdb

con = duckdb.connect()

duplicates = con.execute("""
SELECT
    station_id,
    datetime,
    COUNT(*) AS duplicate_count
FROM read_parquet('lakehouse/silver/wbpcb_master.parquet')
GROUP BY station_id, datetime
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
""").fetchdf()

print(duplicates)

print(f"\nDuplicate Groups: {len(duplicates)}")