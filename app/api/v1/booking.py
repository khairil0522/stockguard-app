
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_permission
from app.errors.auth import RoleNotFoundError
from app.errors.booking import (
    BookingCannotBeCancelledError,
    BookingCannotBeConfirmedError,
    BookingNotFoundError,
    InsufficientQtyError,
    StockNotFoundError,
)
from app.errors.inventory import InventoryNotFoundError
from app.errors.product import ProductNotFoundError
from app.models.users import User
from app.schemas.booking import BookingCreate
from app.services.booking_service import booking_service

router = APIRouter(prefix="/bookings", tags=["Bookings"])

DEPENDENCY_DB = Depends(get_db)
CURRENT_USER = Depends(get_current_user)

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("booking.read"))],
)
async def get_bookings(
    current_user: User = CURRENT_USER,
    db: AsyncSession = DEPENDENCY_DB,
):
    try:
        return await booking_service.get_all(db, current_user.id)
    except RoleNotFoundError as exc:
        raise HTTPException(
            status_code = exc.status_code,
            detail = exc.detail
        )

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("booking.create"))],
)
async def create_booking(
    payload: BookingCreate,
    db: AsyncSession = DEPENDENCY_DB,
    current_user: User = CURRENT_USER,
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
    db: AsyncSession = DEPENDENCY_DB,
    current_user: User = CURRENT_USER,
):
    try:
        await booking_service.confirmed(db, booking_id, current_user.id)
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

DEPENDENCY_DB = Depends(get_db)
CURRENT_USER = Depends(get_current_user)

@router.post(
    "/{booking_id}/cancel",
    dependencies=[Depends(require_permission("booking.cancel"))],
)
async def cancel_booking(
    booking_id: UUID,
    db: AsyncSession = DEPENDENCY_DB,
    current_user: User = CURRENT_USER,
):
    try:
        await booking_service.cancellation(db, booking_id, current_user.id)
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
