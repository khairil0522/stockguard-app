from functools import wraps

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.scheduler.booking_scheduler import process_expired_bookings


def log_scheduler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(">>> Starting StockGuard Scheduler...")
        
        result = func(*args, **kwargs)
        
        print(">>> StockGuard Scheduler started.")
        
        return result

    return wrapper

scheduler = AsyncIOScheduler()

@log_scheduler
def start_scheduler():
    scheduler.add_job(
        process_expired_bookings,
        "interval",
        seconds=30
    )

    scheduler.start()