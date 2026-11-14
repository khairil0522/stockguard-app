from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Inventory, StockMovement, Product
from app.schemas.stock_movement import StockAdjustmentCreate

from app.errors.stock import InsufficientStockError, StockNotFoundError
from app.errors.product import ProductNotFoundError, ProductInactiveError

class StockAdjustmentService:
    async def adjust_stock(
        self,
        db: AsyncSession,
        product_id: UUID,
        payload: StockAdjustmentCreate,
    ) -> StockMovement:
        async with db.begin():
            inventory = await db.scalar(
                select(Inventory)
                .where(Inventory.product_id == product_id)
                .with_for_update()
            )

            if inventory is None:
                raise ProductNotFoundError(product_id)

            product = await db.get(Product, product_id)

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

        return movement

    async def get_data(self, db: AsyncSession):
        statement = (
            select(
                StockMovement,
                Product.name.label("product_name")
            )
            .join(Product, Product.id == StockMovement.product_id)
            .order_by(StockMovement.created_at.desc())
            .limit(5)
        )

        result = await db.execute(statement)
        get_stocks = result.all()

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
        statement = (
            select(
                        StockMovement,
                        Product.name.label("product_name")
                    )
                    .join(Product, Product.id == StockMovement.product_id)
                    .where(StockMovement.product_id == product_id)
                    .order_by(StockMovement.created_at.desc())
        )

        result = await db.execute(statement)
        get_stock = result.all()

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