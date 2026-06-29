from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Existing Data Sources
DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CURATED_DIR = DATA_DIR / "curated"

DATA_METADATA_DIR = DATA_DIR / "metadata"

# Lakehouse Storage
LAKEHOUSE_DIR = PROJECT_ROOT / "lakehouse"

BRONZE_DIR = LAKEHOUSE_DIR / "bronze"
SILVER_DIR = LAKEHOUSE_DIR / "silver"
GOLD_DIR = LAKEHOUSE_DIR / "gold"

LAKEHOUSE_METADATA_DIR = LAKEHOUSE_DIR / "metadata"
LOG_DIR = LAKEHOUSE_DIR / "logs"

# DuckDB
DUCKDB_PATH = LAKEHOUSE_METADATA_DIR / "lakehouse.duckdb"

# =====================================================

SCHEDULE_DAY = "Sunday"

SCHEDULE_TIME = "02:00"

REALTIME_RAW_DIR = RAW_DIR / "realtime"

REALTIME_RAW_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Create Required Directories
for directory in [
    BRONZE_DIR,
    SILVER_DIR,
    GOLD_DIR,
    LAKEHOUSE_METADATA_DIR,
    LOG_DIR,

]:
    directory.mkdir(parents=True, exist_ok=True)