from src.database.connection import get_connection

con = get_connection()

print("=" * 60)
print("Environmental Master")
print("=" * 60)

df = con.execute("""

SELECT *

FROM environmental_master

LIMIT 5;

""").fetchdf()

print(df)

print()

print("=" * 60)
print("Average AQI by Station")
print("=" * 60)

df = con.execute("""

SELECT

station_name,

AVG(aqi) AS avg_aqi

FROM environmental_master

GROUP BY station_name

ORDER BY avg_aqi DESC;

""").fetchdf()

print(df)

con.close()