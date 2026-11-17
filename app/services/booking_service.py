from datetime import datetime, timedelta
from uuid import UUID

from nanoid import generate
from sqlalchemy.ext.asyncio import AsyncSession

from app.audit.booking_audit import BookingAudit
from app.errors.booking import (
    BookingCannotBeCancelledError,
    BookingCannotBeConfirmedError,
    BookingNotFoundError,
    InsufficientQtyError,
    StockNotFoundError,
)
from app.errors.inventory import InventoryNotFoundError
from app.errors.product import ProductNotFoundError
from app.models import Booking, BookingItem, BookingStatus
from app.repositories.booking_repository import booking_repository
from app.repositories.inventory_repository import inventory_repository
from app.repositories.product_repository import product_repository
from app.repositories.user_repository import user_repository
from app.schemas.booking import BookingCreate, BookingItemRead, BookingRead


class BookingService:
    def get_expiry_time(self):
        waktu_sekarang = datetime.now(datetime.UTC)
        waktu_kedaluwarsa = waktu_sekarang + timedelta(minutes=15)
        return waktu_kedaluwarsa

    async def create(self, db: AsyncSession, user_id: UUID, payload: BookingCreate) -> Booking:
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
                product = await product_repository.get_by_id(db, item.product_id)

                if product is None:
                    raise(ProductNotFoundError())

                cek_inventory = await inventory_repository.get_by_product_id_for_update(db, item.product_id)

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

            booking_audit = BookingAudit(db)

            await booking_audit.create(
                user_id=user_id,
                booking_id=booking.id,
                booking_code=booking.booking_code,
                item_count=len(payload.items),
                expired_at=booking.expired_at,
            )
            
            return booking

    async def expired(self, db: AsyncSession, id: UUID):
        waktu_sekarang = datetime.now(datetime.UTC)

        async with db.begin():
            get_booking = await booking_repository.get_by_id_for_update(db, id)

            if get_booking is None:
                raise BookingNotFoundError()

            get_booking_items = await booking_repository.get_items(db, get_booking.id)

            if (
                get_booking.expired_at <= waktu_sekarang
                and get_booking.booking_status == BookingStatus.PENDING
            ):
                get_booking.booking_status = BookingStatus.EXPIRED

                for item in get_booking_items:
                    get_inventory = await inventory_repository.get_by_product_id_for_update(db, item.product_id)

                    if get_inventory is None:
                        raise InventoryNotFoundError()

                    get_inventory.reserved_qty -= item.qty

                booking_audit = BookingAudit(db)

                await booking_audit.expire(
                    booking_id=get_booking.id,
                )

    async def cancellation(self, db: AsyncSession, id: UUID, user_id: UUID):
        failed_booking_code = None
        failed_user_id = None

        try:
            async with db.begin():
                get_booking = await booking_repository.get_by_id_for_update(db, id)

                if get_booking is None:
                    raise BookingNotFoundError()

                get_booking_items = await booking_repository.get_items(db, get_booking.id)

                if get_booking.booking_status == BookingStatus.PENDING:
                    get_booking.booking_status = BookingStatus.CANCELLED

                    for item in get_booking_items:
                        get_inventory = await inventory_repository.get_by_product_id_for_update(db, item.product_id)

                        if get_inventory is None:
                            raise InventoryNotFoundError()

                        get_inventory.reserved_qty -= item.qty

                    booking_audit = BookingAudit(db)

                    await booking_audit.cancel(
                        user_id=user_id,
                        booking_id=get_booking.id,
                        booking_code=get_booking.booking_code,
                    )

                else:
                    failed_booking_code = get_booking.booking_code
                    failed_user_id = get_booking.user_id

                    raise BookingCannotBeCancelledError()

        except BookingCannotBeCancelledError:
            booking_audit = BookingAudit(db)

            await booking_audit.cancel_failed(
                user_id=user_id,
                booking_id=id,
                booking_code=failed_booking_code,
            )

            await db.commit()

            raise

    async def confirmed(self, db: AsyncSession, id: UUID, user_id: UUID):
        failed_booking_code = None
        failed_user_id = None

        try:
            async with db.begin():
                get_booking = await booking_repository.get_by_id_for_update(db, id)

                if get_booking is None:
                    raise BookingNotFoundError()

                get_booking_items = await booking_repository.get_items(db, get_booking.id)

                if get_booking.booking_status == BookingStatus.PENDING:
                    get_booking.booking_status = BookingStatus.CONFIRMED

                    for item in get_booking_items:
                        get_inventory = await inventory_repository.get_by_product_id_for_update(db, item.product_id)

                        if get_inventory is None:
                            raise InventoryNotFoundError()

                        get_inventory.on_hand -= item.qty
                        get_inventory.reserved_qty -= item.qty

                    booking_audit = BookingAudit(db)

                    await booking_audit.confirm(
                        user_id=user_id,
                        booking_id=get_booking.id,
                        booking_code=get_booking.booking_code,
                    )

                else:
                    failed_booking_code = get_booking.booking_code
                    failed_user_id = get_booking.user_id

                    raise BookingCannotBeConfirmedError()

        except BookingCannotBeConfirmedError:
            booking_audit = BookingAudit(db)

            await booking_audit.confirm_failed(
                user_id=user_id,
                booking_id=id,
                booking_code=failed_booking_code,
            )

            await db.commit()

            raise

    async def get_all(self, db: AsyncSession, user_id : UUID):
        role_names = await user_repository.get_role_names(db, user_id)

        if "CUSTOMER" in role_names :
            bookings = await booking_repository.get_all_with_items(db, user_id=user_id)
        else :
            bookings = await booking_repository.get_all_with_items(db)

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
