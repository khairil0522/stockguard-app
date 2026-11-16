from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.products import Product


class ProductRepository:

    async def get_all(self, db: AsyncSession) -> list[Product]:

        result = await db.execute(
            select(Product)
            .order_by(Product.name)
        )

        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, product_id: UUID) -> Product | None:

        return await db.scalar(
            select(Product).where(
                Product.id == product_id
            )
        )

    async def get_by_id_with_inventory(self, db: AsyncSession, product_id: UUID) -> Product | None:

        return await db.scalar(
            select(Product)
            .options(selectinload(Product.inventory))
            .where(Product.id == product_id)
        )

    async def get_by_sku(self, db: AsyncSession, sku: str) -> Product | None:

        return await db.scalar(
            select(Product).where(
                Product.sku == sku
            )
        )


product_repository = ProductRepository()