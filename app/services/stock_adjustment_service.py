from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Inventory, StockMovement, Product
from app.schemas.stock_movement import StockAdjustmentCreate

from app.errors.stock import InsufficientStockError, StockNotFoundError

def adjust_stock(
    db: Session,
    product_id: UUID,
    payload: StockAdjustmentCreate,
) -> StockMovement:
    with db.begin():
        inventory = db.scalar(
            select(Inventory)
            .where(Inventory.product_id == product_id)
            .with_for_update()
        )

        if inventory is None:
            raise ProductNotFoundError(product_id)

        previous_on_hand = inventory.on_hand

        if payload.movement_type == "INCREASE":
            new_on_hand = previous_on_hand + payload.quantity
        else:
            new_on_hand = previous_on_hand - payload.quantity

            if new_on_hand < inventory.reserved_qty:
                raise InsufficientStockError(
                    "Pengurangan stok melebihi stok yang tersedia"
                )

        inventory.on_hand = new_on_hand

        movement = StockMovement(
            product_id=product_id,
            movement_type=payload.movement_type,
            quantity=payload.quantity,
            previous_on_hand=previous_on_hand,
            new_on_hand=new_on_hand,
            reason=payload.reason,
        )

        db.add(movement)
        db.flush()

    return movement

def get_stock_adjustment(db: Session):
    get_stocks = (
        db.query(StockMovement, Product.name.label("product_name"))
        .join(Product, Product.id == StockMovement.product_id)
        .order_by(StockMovement.created_at.desc()).limit(5).all()
    )
    if len(get_stocks) == 0:
        raise(StockNotFoundError())

    return [
        {
            "id": movement.id,
            "product_id": movement.product_id,
            "movement_type": movement.movement_type,
            "quantity": movement.quantity,
            "previous_on_hand": movement.previous_on_hand,
            "new_on_hand": movement.new_on_hand,
            "reason": movement.reason,
            "product_name": product_name,
        }
        for movement, product_name in get_stocks
]

def get_stock_adjustment_by_product(db: Session, product_id: UUID):
    get_stock = (
        db.query(
            StockMovement,
            Product.name.label("product_name")
        )
        .join(Product, Product.id == StockMovement.product_id)
        .where(StockMovement.product_id == product_id)
        .order_by(StockMovement.created_at.desc())
        .all()
    )

    if not get_stock:
        raise StockNotFoundError()

    return [
        {
            "id": movement.id,
            "product_id": movement.product_id,
            "created_at": movement.created_at,
            "movement_type": movement.movement_type,
            "quantity": movement.quantity,
            "reason": movement.reason,
            "product_name": product_name,
        }
        for movement, product_name in get_stock
]