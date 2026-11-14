from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scheduler.booking_scheduler import process_expired_bookings

scheduler = AsyncIOScheduler()

def start_scheduler():
    print(">>> Starting StockGuard Scheduler...")
    scheduler.add_job(
        process_expired_bookings,
        "interval",
        seconds=30
    )

    scheduler.start()
    print(">>> StockGuard Scheduler started.")