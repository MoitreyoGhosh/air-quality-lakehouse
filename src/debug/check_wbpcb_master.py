import duckdb

df = duckdb.sql("""
SELECT *
FROM read_parquet('lakehouse/silver/wbpcb_master.parquet')
LIMIT 5
""").df()

print(df.columns.tolist())
print(df.head())