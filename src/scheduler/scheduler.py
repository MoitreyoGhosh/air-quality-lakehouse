# pyrefly: ignore [missing-import]
import schedule 
import time

from src.scheduler.realtime_pipeline import run

from src.config import SCHEDULE_TIME

schedule.every().sunday.at(
    SCHEDULE_TIME
).do(run)

print("Scheduler Started")

while True:

    schedule.run_pending()

    time.sleep(30)