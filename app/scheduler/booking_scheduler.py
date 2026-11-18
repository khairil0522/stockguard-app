import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from app.db.session import AsyncSessionLocal
from app.errors.booking import BookingNotFoundError
from app.errors.inventory import InventoryNotFoundError
from app.models import Booking, BookingStatus
from app.services.audit_log_service import AuditLogService
from app.services.booking_service import booking_service

logger = logging.getLogger(__name__)


async def process_expired_bookings():
    async with AsyncSessionLocal() as db:
        statement = (
            select(Booking.id)
            .where(
                Booking.booking_status == BookingStatus.PENDING,
                Booking.expired_at <= datetime.now(timezone.utc),  # noqa: UP017
            )
        )

        try:
            result = await db.scalars(statement)

        except OperationalError as exc:
            logger.error(
                "Database connection error while processing expired bookings: %s",
                exc,
            )
            return
        booking_ids = result.all()

        for booking_id in booking_ids:
            async with AsyncSessionLocal() as item_db:
                try:
                    await booking_service.expired(item_db, booking_id)

                    await AuditLogService.log(
                        item_db,
                        actor_type="SYSTEM",
                        event_type="ACTIVITY",
                        action="EXPIRE_BOOKING",
                        entity_type="BOOKING",
                        entity_id=booking_id,
                        description=f"Booking {booking_id} expired automatically by scheduler",
                        severity="INFO",
                    )
                except (BookingNotFoundError, InventoryNotFoundError) as e:
                    logger.error(
                        "Gagal expire booking %s: %s",
                        booking_id,
                        e,
                    )
                    continue