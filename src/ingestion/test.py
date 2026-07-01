from src.config import RAW_DIR
from src.ingestion.historical import HistoricalIngestion

ingestion = HistoricalIngestion()

datasets = ingestion.ingest(
    connector_name="wbpcb",
    source=RAW_DIR,
)

print(ingestion.summary(datasets))
print(next(iter(datasets.values())).columns.tolist())

datasets = ingestion.ingest(
    connector_name="openmeteo",
    source=RAW_DIR / "open-meteo-weather",
)

print(ingestion.summary(datasets))
print(next(iter(datasets.values())).columns.tolist())