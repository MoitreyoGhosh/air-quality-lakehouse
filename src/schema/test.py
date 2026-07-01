"""
Schema pipeline test
"""

from src.config import RAW_DIR, REPORTS_DIR
from src.schema.discover import SchemaDiscovery
from src.schema.mapper import SchemaMapper

discovery = SchemaDiscovery()
mapper = SchemaMapper()


# =====================================================
# WBPCB
# =====================================================

print("=" * 80)
print("WBPCB")
print("=" * 80)

wbpcb = discovery.discover(
    connector_name="wbpcb",
    source=RAW_DIR,
)

discovery.print_report(wbpcb)

print("\nCommon Columns")
print(discovery.common_columns(wbpcb))


# Test mapping on first dataset
dataset_name = next(iter(wbpcb.keys()))

print("\nTesting Mapping:", dataset_name)

from src.connectors.wbpcb import WBPCBConnector

connector = WBPCBConnector(RAW_DIR)
connector.connect()

df = connector.read_all()[dataset_name]

mapped_df, report = mapper.map(df)

print("\nMapped Columns")
print(mapped_df.columns.tolist())

print("\nMapping Report")
print(mapper.report(report))


# =====================================================
# Open-Meteo
# =====================================================

print("\n\n" + "=" * 80)
print("OPENMETEO")
print("=" * 80)

weather = discovery.discover(
    connector_name="openmeteo",
    source=RAW_DIR / "open-meteo-weather",
)

discovery.print_report(weather)

print("\nCommon Columns")
print(discovery.common_columns(weather))


dataset_name = next(iter(weather.keys()))

from src.connectors.openmeteo import OpenMeteoConnector

connector = OpenMeteoConnector(
    RAW_DIR / "open-meteo-weather"
)

connector.connect()

df = connector.read_all()[dataset_name]

mapped_df, report = mapper.map(df)

print("\nMapped Columns")
print(mapped_df.columns.tolist())

print("\nMapping Report")
print(mapper.report(report))

