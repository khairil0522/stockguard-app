from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.audit.adjustment_audit import AdjustmentAudit
from app.errors.product import ProductInactiveError, ProductNotFoundError
from app.errors.stock import InsufficientStockError, StockNotFoundError
from app.models import StockMovement
from app.repositories.inventory_repository import inventory_repository
from app.repositories.product_repository import product_repository
from app.repositories.stock_movement_repository import stock_movement_repository
from app.schemas.stock_movement import StockAdjustmentCreate


class StockAdjustmentService:
    async def adjust_stock(self, db: AsyncSession, product_id: UUID, payload: StockAdjustmentCreate, user_id: UUID) -> StockMovement:
        try:
            async with db.begin():
                inventory = await inventory_repository.get_by_product_id_for_update(db, product_id)

                if inventory is None:
                    raise ProductNotFoundError(product_id)

                product = await product_repository.get_by_id(db, product_id)

                if product is None:
                    raise ProductNotFoundError()

                if not product.is_active:
                    raise ProductInactiveError("Produk tidak aktif, tidak dapat melakukan penyesuaian stok")

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
                await db.flush()

                adjustment_audit = AdjustmentAudit(db)

                await adjustment_audit.adjust(
                    user_id=user_id,
                    product_id=product_id,
                    sku=product.sku,
                    movement_type=payload.movement_type,
                    quantity=payload.quantity,
                    previous_on_hand=previous_on_hand,
                    new_on_hand=new_on_hand,
                    reserved_qty=inventory.reserved_qty,
                    reason=payload.reason,
                )

            return movement
        
        except InsufficientStockError:
            adjustment_audit = AdjustmentAudit(db)

            await adjustment_audit.adjust_failed(
                user_id=user_id,
                product_id=product_id,
                movement_type=payload.movement_type,
                quantity=payload.quantity,
                reason=payload.reason,
            )

            await db.commit()

            raise

    async def get_data(self, db: AsyncSession):
        get_stocks = await stock_movement_repository.get_recent_with_product_name(db, limit=5)

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

    async def get_by_product(self, db: AsyncSession, product_id: UUID):
        get_stock = await stock_movement_repository.get_by_product_with_product_name(db, product_id)

        if not get_stock:
            return []

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

stockadjustment_service = StockAdjustmentService()