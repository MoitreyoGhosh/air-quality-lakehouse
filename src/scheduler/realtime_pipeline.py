# pyrefly: ignore [missing-import]
from src.realtime.fetcher import collect_realtime_data

from src.lakehouse.bronze import run as bronze

from src.lakehouse.silver import run as silver

from src.lakehouse.gold import run as gold

from src.database.views import create_views

from src.database.dataset_views import create_dataset_views

from src.scheduler.logger import write_log


def run():

    write_log("Realtime Pipeline Started")

    collect_realtime_data()

    bronze()

    silver()

    gold()

    create_views()

    create_dataset_views()

    write_log("Realtime Pipeline Completed")