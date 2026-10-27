from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from nanoid import generate
from uuid import UUID
from app.errors.product import ProductNotFoundError
from app.errors.booking import (
    StockNotFoundError,
    InventoryNotFoundError,
    InsufficientQtyError,
    BookingCannotBeCancelledError,
    BookingCannotBeConfirmedError,
    BookingNotFoundError
)

from app.models import Booking, BookingItem, BookingStatus, Product, Inventory
from app.schemas.booking import BookingCreate, BookingItemCreate

def get_expiry_time():
    waktu_sekarang = datetime.now(timezone.utc)
    waktu_kedaluwarsa = waktu_sekarang + timedelta(minutes=15)
    return waktu_kedaluwarsa

def create_booking_with_items(
    db: Session,
    payload: BookingCreate,
    ) -> Booking:
    with db.begin():
        BOOKING_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        booking = Booking(
            booking_code = generate(alphabet=BOOKING_ALPHABET, size=30),
            booking_status = BookingStatus.PENDING,
            expired_at = get_expiry_time()
        )

        db.add(booking)
        db.flush()

        for item in payload.items:
            product = db.scalar(
                select(Product).where(Product.id == item.product_id)
            )

            if product is None:
                raise(ProductNotFoundError())

            cek_inventory = db.scalar(
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

def expired_booking(db: Session, id: UUID):
    waktu_sekarang = datetime.now(timezone.utc)

    with db.begin():
        get_booking = db.scalar(
            select(Booking).where(Booking.id == id).with_for_update()
        )

        if get_booking is None :
            raise(BookingNotFoundError())

        get_booking_items = db.scalars(
            select(BookingItem).where(BookingItem.booking_id == get_booking.id)
        ).all()

        if get_booking.expired_at <= waktu_sekarang and get_booking.booking_status == BookingStatus.PENDING:
            get_booking.booking_status = BookingStatus.EXPIRED

            for item in get_booking_items:
                get_inventory = db.scalar(
                    select(Inventory).where(Inventory.product_id == item.product_id).with_for_update()
                )

                if get_inventory is None :
                    raise(InventoryNotFoundError())

                get_inventory.reserved_qty -= item.qty

def cancellation_booking(db: Session, id:UUID):
    with db.begin():
        get_booking = db.scalar(
            select(Booking).where(Booking.id == id).with_for_update()
        )

        if get_booking is None:
            raise(BookingNotFoundError())
        
        get_booking_items = db.scalars(
            select(BookingItem).where(BookingItem.booking_id == get_booking.id)
        ).all()

        if get_booking.booking_status == BookingStatus.PENDING:
            get_booking.booking_status = BookingStatus.CANCELLED

            for item in get_booking_items:
                get_inventory = db.scalar(
                    select(Inventory).where(Inventory.product_id == item.product_id).with_for_update()
                )

                if get_inventory is None :
                    raise(InventoryNotFoundError())

                get_inventory.reserved_qty -= item.qty
        
        else:
            raise(BookingCannotBeCancelledError())

def confirmed_booking(db: Session, id:UUID):
    with db.begin():
        get_booking = db.scalar(
            select(Booking).where(Booking.id == id).with_for_update()
        )

        if get_booking is None:
            raise(BookingNotFoundError())
        
        get_booking_items = db.scalars(
            select(BookingItem).where(BookingItem.booking_id == get_booking.id)
        ).all()

        if get_booking.booking_status == BookingStatus.PENDING:
            get_booking.booking_status = BookingStatus.CONFIRMED

            for item in get_booking_items:
                get_inventory = db.scalar(
                    select(Inventory).where(Inventory.product_id == item.product_id).with_for_update()
                )

                if get_inventory is None :
                    raise(InventoryNotFoundError())

                get_inventory.on_hand -= item.qty
                get_inventory.reserved_qty -= item.qty
    
        else :
            raise(BookingCannotBeConfirmedError())