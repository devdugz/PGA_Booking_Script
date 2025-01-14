from apscheduler.schedulers.blocking import BlockingScheduler
from pga_booking import book_golf_bay
import logging
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('/Users/cdugz/Documents/PGA_Booking_Script_2/logs/scheduler.log'),
        logging.StreamHandler()
    ],
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def scheduled_job():
    try:
        logger.info(f"Starting scheduled booking attempt at {datetime.now()}")
        success = book_golf_bay()  # Capture return value
        if success:  # Only shutdown on actual success
            logger.info("Booking attempt completed successfully")
            logger.info("Booking successful - stopping scheduler")
            scheduler.remove_all_jobs()
            scheduler.shutdown(wait=False)
        else:
            logger.info("Booking attempt failed - continuing schedule")
    except Exception as e:
        logger.error(f"Booking attempt failed: {str(e)}")

scheduler = BlockingScheduler()

# Add jobs for every 15 minutes between 1 AM and 9 AM
for hour in range(0, 24):
    for minute in [0, 15, 30, 45]:
        scheduler.add_job(scheduled_job, 'cron', hour=hour, minute=minute)
        logger.info(f"Scheduled job for {hour:02d}:{minute:02d}")

if __name__ == '__main__':
    try:
        logger.info("Starting scheduler")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped")