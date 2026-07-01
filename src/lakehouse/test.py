# """
# test.py
# =====================================

# Lakehouse Test Suite

# Tests
# -----
# ✓ Bronze layer
# ✓ Silver layer
# ✓ Metadata
# ✓ Cleaning report
# ✓ Integrated datasets
# """

# from __future__ import annotations

# import pandas as pd

# from src.database.init_db import initialize_database
# from src.database.connection import database
# from src.database.utils import DatabaseUtils
# from src.lakehouse.bronze import bronze
# from src.lakehouse.silver import silver


# def line():
#     print("=" * 80)


# def section(title: str):
#     line()
#     print(title)
#     line()


# def show_tables(schema: str):

#     print(f"\n{schema.upper()} TABLES")
#     print("-" * 80)

#     tables = DatabaseUtils.list_tables(schema)

#     for table in sorted(tables):
#         print(table)

#     print(f"\nTotal Tables : {len(tables)}")

#     return tables


# def describe_table(schema: str, table: str):

#     print(f"\n{schema}.{table}")

#     print("-" * 80)

#     columns = database.connection.execute(
#         f"""
#         DESCRIBE {schema}.{table}
#         """
#     ).fetchdf()

#     print(columns)

#     rows = database.connection.execute(
#         f"""
#         SELECT COUNT(*)
#         FROM {schema}.{table}
#         """
#     ).fetchone()[0]

#     print(f"\nRows : {rows}")


# def preview(schema: str, table: str, limit: int = 5):

#     print("\nPreview")

#     print("-" * 80)

#     df = database.connection.execute(
#         f"""
#         SELECT *
#         FROM {schema}.{table}
#         LIMIT {limit}
#         """
#     ).fetchdf()

#     print(df)


# def bronze_summary():

#     section("BRONZE SUMMARY")

#     print(bronze.summary())


# def silver_summary():

#     section("SILVER PIPELINE")

#     summary = silver.run()

#     print(summary)

#     return summary


# def metadata_report():

#     section("CLEANING REPORT")

#     try:

#         report = database.connection.execute(
#             """
#             SELECT *
#             FROM metadata.cleaning_report
#             ORDER BY source, station
#             """
#         ).fetchdf()

#         print(report)

#     except Exception:

#         print("No cleaning report found.")


# def inspect_station(station: str):

#     section(f"INSPECTING STATION : {station}")

#     wbpcb = f"wbpcb_{station}"
#     weather = f"openmeteo_{station}"
#     integrated = f"integrated_{station}"

#     for table in [wbpcb, weather, integrated]:

#         try:

#             describe_table(
#                 "silver",
#                 table,
#             )

#             preview(
#                 "silver",
#                 table,
#             )

#         except Exception:

#             print(f"{table} not found.")


# def integrated_statistics():

#     section("INTEGRATED DATASETS")

#     tables = DatabaseUtils.list_tables("silver")

#     integrated = sorted(
#         table
#         for table in tables
#         if table.startswith("integrated_")
#     )

#     stats = []

#     for table in integrated:

#         rows = database.connection.execute(
#             f"""
#             SELECT COUNT(*)
#             FROM silver.{table}
#             """
#         ).fetchone()[0]

#         cols = database.connection.execute(
#             f"""
#             DESCRIBE silver.{table}
#             """
#         ).fetchdf()

#         stats.append(
#             {
#                 "dataset": table,
#                 "rows": rows,
#                 "columns": len(cols),
#             }
#         )

#     print(pd.DataFrame(stats))


# def main():

#     initialize_database()

#     bronze.initialize()

#     section("BRONZE LAYER")

#     bronze_tables = show_tables("bronze")

#     bronze_summary()

#     section("RUN SILVER")

#     silver_summary()

#     section("SILVER TABLES")

#     silver_tables = show_tables("silver")

#     metadata_report()

#     # Inspect the first integrated station

#     integrated = [
#         t
#         for t in silver_tables
#         if t.startswith("integrated_")
#     ]

#     if integrated:

#         station = integrated[0].replace(
#             "integrated_",
#             "",
#         )

#         inspect_station(station)

#     integrated_statistics()

#     section("TEST COMPLETED")


# if __name__ == "__main__":

#     main()