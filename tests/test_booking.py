import pytest

from uuid import uuid4
from sqlalchemy import select

from app.models import (
    Booking,
    BookingItem,
    BookingStatus,
    Product,
    Inventory,
)

from datetime import datetime, timedelta, timezone
from app.services.booking_service import (
    create_booking_with_items,
    InsufficientQtyError,
    expired_booking,
    cancellation_booking,
    BookingCannotBeCancelledError,
    confirmed_booking,
    BookingCannotBeConfirmedError
)
from app.schemas.booking import BookingCreate, BookingItemCreate

def test_booking_success(db_session):
    now = datetime.now(timezone.utc)
    products = [
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Komputer",
        unit_price=350000,),
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Mouse",
        unit_price=125000,)
    ]

    db_session.add_all(products)
    db_session.flush()

    inventories = [
        Inventory(
            product_id=products[0].id,
            on_hand=10,
            reserved_qty=0,),
        Inventory(
            product_id=products[1].id,
            on_hand=15,
            reserved_qty=0,)
    ]
    db_session.add_all(inventories)
    db_session.flush()

    db_session.commit()

    #Booking payload
    payload = BookingCreate(
        items=[
            BookingItemCreate(
                product_id=products[0].id,
                qty=2,
            ),
            BookingItemCreate(
                product_id=products[1].id,
                qty=2,
            ),
        ]
    )

    booking = create_booking_with_items(db_session, payload)

    db_session.refresh(inventories[0])
    db_session.refresh(inventories[1])

    items_by_product = {
        item.product_id: item for item in booking.items
    }

    assert booking.id is not None
    assert booking.booking_code is not None
    assert booking.booking_status == BookingStatus.PENDING
    assert booking.expired_at > now + timedelta(minutes=14)
    assert booking.expired_at <= now + timedelta(minutes=16)
    assert len(booking.items) == 2
    assert items_by_product[products[0].id].unit_price == 350000
    assert items_by_product[products[1].id].unit_price == 125000
    assert inventories[0].reserved_qty == 2
    assert inventories[1].reserved_qty == 2
    assert inventories[0].on_hand == 10
    assert inventories[1].on_hand == 15

def test_booking_failure(db_session):
    now = datetime.now(timezone.utc)
    products = [
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Komputer",
        unit_price=350000,),
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Mouse",
        unit_price=125000,)
    ]

    db_session.add_all(products)
    db_session.flush()

    inventories = [
        Inventory(
            product_id=products[0].id,
            on_hand=10,
            reserved_qty=9,),
        Inventory(
            product_id=products[1].id,
            on_hand=15,
            reserved_qty=12,)
    ]
    db_session.add_all(inventories)
    db_session.flush()

    db_session.commit()

    #Booking payload
    payload = BookingCreate(
        items=[
            BookingItemCreate(
                product_id=products[0].id,
                qty=5,
            ),
            BookingItemCreate(
                product_id=products[1].id,
                qty=5,
            ),
        ]
    )

    with pytest.raises(InsufficientQtyError):
        create_booking_with_items(db_session, payload)

    assert db_session.scalars(select(Booking)).all() == []
    assert db_session.scalars(select(BookingItem)).all() == []

    assert inventories[0].reserved_qty == 9
    assert inventories[1].reserved_qty == 12
    assert inventories[0].on_hand == 10
    assert inventories[1].on_hand == 15

def test_expired_booking(db_session):
    now = datetime.now(timezone.utc)
    products = [
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Komputer",
        unit_price=350000,),
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Mouse",
        unit_price=125000,)
    ]

    db_session.add_all(products)
    db_session.flush()

    inventories = [
        Inventory(
            product_id=products[0].id,
            on_hand=10,
            reserved_qty=0,),
        Inventory(
            product_id=products[1].id,
            on_hand=15,
            reserved_qty=0,)
    ]
    db_session.add_all(inventories)
    db_session.flush()

    db_session.commit()

    #Booking payload
    payload = BookingCreate(
        items=[
            BookingItemCreate(
                product_id=products[0].id,
                qty=2,
            ),
            BookingItemCreate(
                product_id=products[1].id,
                qty=2,
            ),
        ]
    )

    booking = create_booking_with_items(db_session, payload)
    booking.expired_at = datetime.now(timezone.utc) - timedelta(minutes=15)
    db_session.commit()

    expired_booking(db_session, booking.id)

    assert booking.booking_status == BookingStatus.EXPIRED
    
    for invent in inventories :
        assert invent.reserved_qty == 0

def test_cancellation_booking(db_session):
    now = datetime.now(timezone.utc)
    products = [
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Komputer",
        unit_price=350000,),
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Mouse",
        unit_price=125000,)
    ]

    db_session.add_all(products)
    db_session.flush()

    inventories = [
        Inventory(
            product_id=products[0].id,
            on_hand=10,
            reserved_qty=0,),
        Inventory(
            product_id=products[1].id,
            on_hand=15,
            reserved_qty=0,)
    ]
    db_session.add_all(inventories)
    db_session.flush()

    db_session.commit()

    #Booking payload
    payload = BookingCreate(
        items=[
            BookingItemCreate(
                product_id=products[0].id,
                qty=5,
            ),
            BookingItemCreate(
                product_id=products[1].id,
                qty=5,
            ),
        ]
    )

    booking = create_booking_with_items(db_session, payload)
    cancellation_booking(db_session, booking.id)

    assert booking.booking_status == BookingStatus.CANCELLED
    for invent in inventories :
        assert invent.reserved_qty == 0

def test_cannot_cancellation_booking(db_session):
    now = datetime.now(timezone.utc)
    products = [
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Komputer",
        unit_price=350000,),
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Mouse",
        unit_price=125000,)
    ]

    db_session.add_all(products)
    db_session.flush()

    inventories = [
        Inventory(
            product_id=products[0].id,
            on_hand=10,
            reserved_qty=0,),
        Inventory(
            product_id=products[1].id,
            on_hand=15,
            reserved_qty=0,)
    ]
    db_session.add_all(inventories)
    db_session.flush()

    db_session.commit()

    #Booking payload
    payload = BookingCreate(
        items=[
            BookingItemCreate(
                product_id=products[0].id,
                qty=5,
            ),
            BookingItemCreate(
                product_id=products[1].id,
                qty=5,
            ),
        ]
    )

    booking = create_booking_with_items(db_session, payload)
    cancellation_booking(db_session, booking.id)

    with pytest.raises(BookingCannotBeCancelledError):
        cancellation_booking(db_session, booking.id)

    assert booking.booking_status == BookingStatus.CANCELLED

    for invent in inventories:
        assert invent.reserved_qty == 0

def test_cannot_cancellation_booking_expired(db_session):
    now = datetime.now(timezone.utc)
    products = [
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Komputer",
        unit_price=350000,),
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Mouse",
        unit_price=125000,)
    ]

    db_session.add_all(products)
    db_session.flush()

    inventories = [
        Inventory(
            product_id=products[0].id,
            on_hand=10,
            reserved_qty=0,),
        Inventory(
            product_id=products[1].id,
            on_hand=15,
            reserved_qty=0,)
    ]
    db_session.add_all(inventories)
    db_session.flush()

    db_session.commit()

    #Booking payload
    payload = BookingCreate(
        items=[
            BookingItemCreate(
                product_id=products[0].id,
                qty=5,
            ),
            BookingItemCreate(
                product_id=products[1].id,
                qty=5,
            ),
        ]
    )

    booking = create_booking_with_items(db_session, payload)
    booking.expired_at = datetime.now(timezone.utc) - timedelta(minutes=15)
    db_session.commit()

    expired_booking(db_session, booking.id)

    with pytest.raises(BookingCannotBeCancelledError):
        cancellation_booking(db_session, booking.id)

    assert booking.booking_status == BookingStatus.EXPIRED

    for invent in inventories:
        assert invent.reserved_qty == 0

def test_confirm_booking_success(db_session):
    now = datetime.now(timezone.utc)
    products = [
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Komputer",
        unit_price=350000,),
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Mouse",
        unit_price=125000,)
    ]

    db_session.add_all(products)
    db_session.flush()

    inventories = [
        Inventory(
            product_id=products[0].id,
            on_hand=10,
            reserved_qty=0,),
        Inventory(
            product_id=products[1].id,
            on_hand=15,
            reserved_qty=0,)
    ]
    db_session.add_all(inventories)
    db_session.flush()

    db_session.commit()

    #Booking payload
    payload = BookingCreate(
        items=[
            BookingItemCreate(
                product_id=products[0].id,
                qty=5,
            ),
            BookingItemCreate(
                product_id=products[1].id,
                qty=5,
            ),
        ]
    )

    booking = create_booking_with_items(db_session, payload)
    confirmed_booking(db_session, booking.id)

    assert booking.booking_status == BookingStatus.CONFIRMED
    assert inventories[0].on_hand == 5
    assert inventories[1].on_hand == 10

    for invent in inventories:
        assert invent.reserved_qty == 0

def test_cannot_confirm_booking_confirmed(db_session):
    now = datetime.now(timezone.utc)
    products = [
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Komputer",
        unit_price=350000,),
        Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Mouse",
        unit_price=125000,)
    ]

    db_session.add_all(products)
    db_session.flush()

    inventories = [
        Inventory(
            product_id=products[0].id,
            on_hand=10,
            reserved_qty=0,),
        Inventory(
            product_id=products[1].id,
            on_hand=15,
            reserved_qty=0,)
    ]
    db_session.add_all(inventories)
    db_session.flush()

    db_session.commit()

    #Booking payload
    payload = BookingCreate(
        items=[
            BookingItemCreate(
                product_id=products[0].id,
                qty=5,
            ),
            BookingItemCreate(
                product_id=products[1].id,
                qty=5,
            ),
        ]
    )

    booking = create_booking_with_items(db_session, payload)
    confirmed_booking(db_session, booking.id)

    with pytest.raises(BookingCannotBeConfirmedError):
        confirmed_booking(db_session, booking.id)

    assert booking.booking_status == BookingStatus.CONFIRMED