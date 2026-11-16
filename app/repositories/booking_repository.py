from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.bookings import Booking
from app.models.booking_items import BookingItem


class BookingRepository:

    async def get_by_id_for_update(self, db: AsyncSession, booking_id: UUID) -> Booking | None:

        result = await db.execute(
            select(Booking)
            .where(Booking.id == booking_id)
            .with_for_update()
        )

        return result.scalar_one_or_none()

    async def get_items(self, db: AsyncSession, booking_id: UUID) -> list[BookingItem]:

        result = await db.execute(
            select(BookingItem)
            .where(BookingItem.booking_id == booking_id)
        )

        return result.scalars().all()

    async def get_all(self, db: AsyncSession) -> list[Booking]:

        result = await db.execute(
            select(Booking)
            .order_by(Booking.created_at.desc())
        )

        return result.scalars().all()


booking_repository = BookingRepository()