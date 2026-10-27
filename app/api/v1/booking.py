
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.booking import BookingCreate
from app.services.booking_service import (
    cancellation_booking,
    confirmed_booking,
    create_booking_with_items
)
from app.errors.booking import (
    StockNotFoundError,
    InventoryNotFoundError,
    InsufficientQtyError,
    BookingCannotBeCancelledError,
    BookingCannotBeConfirmedError,
    BookingNotFoundError
)

from app.errors.product import ProductNotFoundError

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_booking_with_items(db, payload)
    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )
    except (StockNotFoundError, InventoryNotFoundError) as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )
    except InsufficientQtyError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )


@router.post("/{booking_id}/confirm")
def confirm_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        confirmed_booking(db, booking_id)
        return {
            "message": "Booking confirmed"
        }
    except BookingNotFoundError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )
    except BookingCannotBeConfirmedError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )
    except InventoryNotFoundError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )


@router.post("/{booking_id}/cancel")
def cancel_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        cancellation_booking(db, booking_id)
        return {
            "message": "Booking cancelled"
        }
    except BookingNotFoundError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )
    except BookingCannotBeCancelledError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )
    except InventoryNotFoundError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )
