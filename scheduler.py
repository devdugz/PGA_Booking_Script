from apscheduler.schedulers.blocking import BlockingScheduler
from pga_booking import book_golf_bay
import logging

logging.basicConfig(level=logging.INFO)

scheduler = BlockingScheduler()

# Add jobs for every 15 minutes between 1 AM and 9 AM
for hour in range(1, 11):
    for minute in [0, 15, 30, 45]:
        scheduler.add_job(book_golf_bay, 'cron', hour=hour, minute=minute)

if __name__ == '__main__':
    scheduler.start()