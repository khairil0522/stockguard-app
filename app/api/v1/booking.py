
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.booking import BookingCreate
from app.services.booking_service import booking_service
from app.errors.booking import (
    StockNotFoundError,
    InsufficientQtyError,
    BookingCannotBeCancelledError,
    BookingCannotBeConfirmedError,
    BookingNotFoundError
)
from app.errors.product import ProductNotFoundError
from app.errors.inventory import InventoryNotFoundError

from app.models.users import User
from app.dependencies.auth import get_current_user, require_permission

from app.errors.product import ProductNotFoundError

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("booking.read"))],
)
async def get_bookings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await booking_service.get_all(db, current_user.id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("booking.create"))],
)
async def create_booking(
    payload: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await booking_service.create(db, current_user.id, payload)
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


@router.post(
    "/{booking_id}/confirm",
    dependencies=[Depends(require_permission("booking.confirm"))],
)
async def confirm_booking(
    booking_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        await booking_service.confirmed(db, booking_id)
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


@router.post(
    "/{booking_id}/cancel",
    dependencies=[Depends(require_permission("booking.cancel"))],
)
async def cancel_booking(
    booking_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        await booking_service.cancellation(db, booking_id)
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
