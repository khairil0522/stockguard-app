
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors.inventory import InventoryNotFoundError
from app.repositories.inventory_repository import inventory_repository
from app.schemas.inventory import InventoryDetailRead, InventoryListRead


class InventoryService:
    async def get_all(self, db: AsyncSession):
        # Ambil inventory beserta relasi Product
        inventory_list = await inventory_repository.get_all_with_product(db)

        if not inventory_list:
            raise InventoryNotFoundError()

        # Mapping ORM object ke response schema
        return [
            InventoryListRead(
                product_id=inventory.product_id,
                sku=inventory.product.sku,
                product_name=inventory.product.name,
                on_hand=inventory.on_hand,
                available_qty=inventory.available_qty,
                is_active=inventory.product.is_active
            )
            for inventory in inventory_list
        ]

    async def get_by_id(self, db: AsyncSession, product_id: UUID):
        # Ambil inventory beserta relasi Product
        get_inventory = await inventory_repository.get_by_product_id_with_product(db, product_id)

        if get_inventory is None:
            raise InventoryNotFoundError()

        # Mapping ORM object ke response schema
        inventory = InventoryDetailRead(
            product_id=get_inventory.product_id,
            sku=get_inventory.product.sku,
            product_name=get_inventory.product.name,
            on_hand=get_inventory.on_hand,
            reserved_qty=get_inventory.reserved_qty,
            description=get_inventory.product.description,
            available_qty=get_inventory.available_qty,
            updated_at=get_inventory.updated_at,
        )

        return inventory

inventory_service = InventoryService()