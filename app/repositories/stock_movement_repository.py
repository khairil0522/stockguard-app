from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Product
from app.models.stock_movement import StockMovement


class StockMovementRepository:

    async def get_recent_with_product_name(self, db: AsyncSession, limit: int):

        result = await db.execute(
            select(StockMovement, Product.name)
            .join(
                Product,
                Product.id == StockMovement.product_id,
            )
            .order_by(
                StockMovement.created_at.desc()
            )
            .limit(limit)
        )

        return result.all()

    async def get_by_product_with_product_name(self, db: AsyncSession, product_id: UUID):

        result = await db.execute(
            select(StockMovement, Product.name)
            .join(
                Product,
                Product.id == StockMovement.product_id,
            )
            .where(
                StockMovement.product_id == product_id
            )
            .order_by(
                StockMovement.created_at.desc()
            )
        )

        return result.all()


stock_movement_repository = StockMovementRepository()