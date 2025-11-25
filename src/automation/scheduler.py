import schedule
import time
from ..core.logger import logger

def run_scheduler():
    """
    Runs the schedule loop.
    """
    logger.info("Starting scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)

def schedule_daily_report(job_func, time_str: str = "08:00"):
    """
    Schedules a job to run daily at a specific time.
    """
    logger.info(f"Scheduling daily report for {time_str}")
    schedule.every().day.at(time_str).do(job_func)
