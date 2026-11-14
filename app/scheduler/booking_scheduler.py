from datetime import datetime, timezone
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models import Booking, BookingStatus
from app.services.booking_service import booking_service
from app.errors.booking import BookingExpirationError, BookingNotFoundError
from app.errors.inventory import InventoryNotFoundError

async def process_expired_bookings():
    async with AsyncSessionLocal() as db:
        statement = (
            select(Booking.id)
            .where(
                Booking.booking_status == BookingStatus.PENDING,
                Booking.expired_at <= datetime.now(timezone.utc),
            )
        )

        result = await db.scalars(statement)
        booking_ids = result.all()

        for booking_id in booking_ids:
            async with AsyncSessionLocal() as item_db:
                try :
                    await booking_service.expired(item_db, booking_id)
                except (BookingNotFoundError, InventoryNotFoundError) as e:
                    raise BookingExpirationError(
                        f"Gagal expire booking {booking_id}"
                    ) from e