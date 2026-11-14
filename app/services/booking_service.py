from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from nanoid import generate
from uuid import UUID
from app.errors.product import ProductNotFoundError
from app.errors.inventory import InventoryNotFoundError
from app.errors.booking import (
    StockNotFoundError,
    InsufficientQtyError,
    BookingCannotBeCancelledError,
    BookingCannotBeConfirmedError,
    BookingNotFoundError
)

from app.models import Booking, BookingItem, BookingStatus, Product, Inventory, Role, UserRole
from app.schemas.booking import BookingCreate, BookingItemCreate, BookingRead, BookingItemRead

class BookingService:
    def get_expiry_time(self):
        waktu_sekarang = datetime.now(timezone.utc)
        waktu_kedaluwarsa = waktu_sekarang + timedelta(minutes=15)
        return waktu_kedaluwarsa

    async def create(
        self,
        db: AsyncSession,
        user_id: UUID,
        payload: BookingCreate,
        ) -> Booking:
        async with db.begin():
            BOOKING_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

            booking = Booking(
                booking_code = generate(alphabet=BOOKING_ALPHABET, size=30),
                booking_status = BookingStatus.PENDING,
                user_id = user_id,
                expired_at = self.get_expiry_time()
            )

            db.add(booking)
            await db.flush()

            for item in payload.items:
                product = await db.scalar(
                    select(Product).where(Product.id == item.product_id)
                )

                if product is None:
                    raise(ProductNotFoundError())

                cek_inventory = await db.scalar(
                    select(Inventory).where(Inventory.product_id == product.id).with_for_update()
                )

                if cek_inventory is None :
                    raise(StockNotFoundError())

                if item.qty > cek_inventory.on_hand - cek_inventory.reserved_qty:
                    raise(InsufficientQtyError())

                booking_items = BookingItem(
                    booking_id = booking.id,
                    product_id = item.product_id,
                    qty = item.qty,
                    unit_price = product.unit_price
                )

                db.add(booking_items)

                cek_inventory.reserved_qty += booking_items.qty
            
            return booking

    async def expired(self, db: AsyncSession, id: UUID):
        waktu_sekarang = datetime.now(timezone.utc)

        async with db.begin():
            get_booking = await db.scalar(
                select(Booking).where(Booking.id == id).with_for_update()
            )

            if get_booking is None :
                raise(BookingNotFoundError())

            result = await db.scalars(
                select(BookingItem).where(BookingItem.booking_id == get_booking.id)
            )
            get_booking_items = result.all()

            if get_booking.expired_at <= waktu_sekarang and get_booking.booking_status == BookingStatus.PENDING:
                get_booking.booking_status = BookingStatus.EXPIRED

                for item in get_booking_items:
                    get_inventory = await db.scalar(
                        select(Inventory).where(Inventory.product_id == item.product_id).with_for_update()
                    )

                    if get_inventory is None :
                        raise(InventoryNotFoundError())

                    get_inventory.reserved_qty -= item.qty

    async def cancellation(self, db: AsyncSession, id:UUID):
        async with db.begin():
            get_booking = await db.scalar(
                select(Booking).where(Booking.id == id).with_for_update()
            )

            if get_booking is None:
                raise(BookingNotFoundError())
            
            result = await db.scalars(
                select(BookingItem).where(BookingItem.booking_id == get_booking.id)
            )
            get_booking_items = result.all()

            if get_booking.booking_status == BookingStatus.PENDING:
                get_booking.booking_status = BookingStatus.CANCELLED

                for item in get_booking_items:
                    get_inventory = await db.scalar(
                        select(Inventory).where(Inventory.product_id == item.product_id).with_for_update()
                    )

                    if get_inventory is None :
                        raise(InventoryNotFoundError())

                    get_inventory.reserved_qty -= item.qty
            
            else:
                raise(BookingCannotBeCancelledError())

    async def confirmed(self, db: AsyncSession, id:UUID):
        async with db.begin():
            get_booking = await db.scalar(
                select(Booking).where(Booking.id == id).with_for_update()
            )

            if get_booking is None:
                raise(BookingNotFoundError())
            
            result = await db.scalars(
                select(BookingItem).where(BookingItem.booking_id == get_booking.id)
            )
            get_booking_items = result.all()

            if get_booking.booking_status == BookingStatus.PENDING:
                get_booking.booking_status = BookingStatus.CONFIRMED

                for item in get_booking_items:
                    get_inventory = await db.scalar(
                        select(Inventory).where(Inventory.product_id == item.product_id).with_for_update()
                    )

                    if get_inventory is None :
                        raise(InventoryNotFoundError())

                    get_inventory.on_hand -= item.qty
                    get_inventory.reserved_qty -= item.qty
        
            else :
                raise(BookingCannotBeConfirmedError())

    async def get_all(self, db: AsyncSession, user_id : UUID):
        statement = (select(Role.name).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user_id))
        result = await db.scalars(statement)
        role_names = set(result.all())

        if "CUSTOMER" in role_names :
            statement = select(Booking).where(Booking.user_id == user_id).options(selectinload(Booking.items))
        else :
            statement = select(Booking).options(selectinload(Booking.items))
        result = await db.scalars(statement)
        bookings = result.all()

        if not bookings:
            return []

        get_all = []

        for booking in bookings :
            get_all_items = []

            for item in booking.items:
                get_all_items.append(
                    BookingItemRead(
                        product_id = item.product_id,
                        qty = item.qty,
                        unit_price = item.unit_price
                    )
                )
            
            get_all.append(
                BookingRead(
                    id = booking.id,
                    booking_code = booking.booking_code,
                    booking_status = booking.booking_status,
                    user_id = booking.user_id,
                    expired_at = booking.expired_at,
                    created_at = booking.created_at,
                    updated_at = booking.updated_at,
                    items = get_all_items
                )
            )

        return get_all

booking_service = BookingService()