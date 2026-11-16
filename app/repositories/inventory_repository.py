from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.inventory import Inventory


class InventoryRepository:

    async def get_all_with_product(self, db: AsyncSession) -> list[Inventory]:

        result = await db.execute(
            select(Inventory)
            .options(selectinload(Inventory.product))
            .order_by(Inventory.product_id)
        )

        return result.scalars().all()


    async def get_by_product_id_with_product(self, db: AsyncSession, product_id: UUID) -> Inventory | None:

        return await db.scalar(
            select(Inventory)
            .where(Inventory.product_id == product_id)
            .options(selectinload(Inventory.product))
        )

    async def get_by_product_id_for_update(self, db: AsyncSession, product_id: UUID) -> Inventory | None:

        result = await db.execute(
            select(Inventory)
            .where(Inventory.product_id == product_id)
            .with_for_update()
        )

        return result.scalar_one_or_none()


inventory_repository = InventoryRepository()