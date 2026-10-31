from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.stock_movement import (
    StockAdjustmentCreate,
    StockAdjustmentRead,
    StockAdjustmentHistoryRead,
    StockMovementHistoryByProduct
)
from app.services.stock_adjustment_service import (
    adjust_stock, get_stock_adjustment, get_stock_adjustment_by_product
)

from app.errors.product import ProductNotFoundError
from app.errors.stock import InsufficientStockError, StockNotFoundError

from app.models import Inventory

router = APIRouter(prefix="/stocks", tags=["Stock Adjustments"])

@router.post(
    "/products/{product_id}/stock-adjustments",
    response_model=StockAdjustmentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_stock_adjustment(
    product_id: UUID,
    payload: StockAdjustmentCreate,
    db: Session = Depends(get_db),
):
    try:
        movement = adjust_stock(db, product_id, payload)

        return {
            "id": movement.id,
            "product_id": movement.product_id,
            "movement_type": movement.movement_type,
            "quantity": movement.quantity,
            "previous_on_hand": movement.previous_on_hand,
            "new_on_hand": movement.new_on_hand,
            "available_qty": (
                movement.new_on_hand
                - db.get(Inventory, product_id).reserved_qty
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
def get_stocks(
    db: Session = Depends(get_db),
):
    try:
        stock_list = get_stock_adjustment(db)
        return stock_list

    except StockNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )

@router.get(
    "/{product_id}",
    response_model=list[StockMovementHistoryByProduct],
    status_code=status.HTTP_200_OK)
def get_stocks_by_product_id(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        stock_list = get_stock_adjustment_by_product(db, product_id)
        return stock_list
    except StockNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )