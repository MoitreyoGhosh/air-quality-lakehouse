from pathlib import Path
from datetime import datetime

from src.config import LOG_DIR

LOG_FILE = LOG_DIR / "scheduler.log"


def write_log(message: str):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log:

        log.write(f"[{timestamp}] {message}\n")