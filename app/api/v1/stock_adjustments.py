from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.stock_movement import (
    StockAdjustmentCreate,
    StockAdjustmentRead,
    StockAdjustmentHistoryRead,
    StockMovementHistoryByProduct
)
from app.services.stock_adjustment_service import stockadjustment_service

from app.errors.product import ProductNotFoundError
from app.errors.stock import InsufficientStockError, StockNotFoundError

from app.models import Inventory

router = APIRouter(prefix="/stocks", tags=["Stock Adjustments"])

@router.post(
    "/products/{product_id}/stock-adjustments",
    response_model=StockAdjustmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_stock_adjustment(
    product_id: UUID,
    payload: StockAdjustmentCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        movement = await stockadjustment_service.adjust_stock(db, product_id, payload)
        inventory = await db.get(Inventory, product_id)

        return {
            "id": movement.id,
            "product_id": movement.product_id,
            "movement_type": movement.movement_type,
            "quantity": movement.quantity,
            "previous_on_hand": movement.previous_on_hand,
            "new_on_hand": movement.new_on_hand,
            "available_qty": (
                movement.new_on_hand
                - inventory.reserved_qty
            ),
            "reason": movement.reason,
        }

    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except InsufficientStockError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )

@router.get(
    "/",
    response_model=list[StockAdjustmentHistoryRead],
    status_code=status.HTTP_200_OK)
async def get_stocks(
    db: AsyncSession = Depends(get_db),
):
    try:
        return await stockadjustment_service.get_data(db)

    except StockNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )

@router.get(
    "/{product_id}",
    response_model=list[StockMovementHistoryByProduct],
    status_code=status.HTTP_200_OK)
async def get_stocks_by_product_id(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await stockadjustment_service.get_by_product(db, product_id)
    except StockNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )