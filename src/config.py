from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Backward-compatible alias used by older modules.
ROOT_DIR = PROJECT_ROOT

# Existing Data Sources
DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"

DATA_METADATA_DIR = DATA_DIR / "metadata"

# =====================================================

SCHEDULE_DAY = "Sunday"

SCHEDULE_TIME = "02:00"

REALTIME_RAW_DIR = RAW_DIR / "realtime"

REALTIME_RAW_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# REPORTS
REPORTS_DIR = PROJECT_ROOT / "reports"