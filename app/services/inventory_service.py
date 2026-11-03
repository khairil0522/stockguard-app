from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import Inventory, Product
from app.errors.inventory import InventoryNotFoundError
from app.schemas.inventory import InventoryListRead, InventoryDetailRead

def get_all_inventory(db: Session):
    # Ambil inventory beserta relasi Product
    statement = (
        select(Inventory)
        .options(selectinload(Inventory.product))   
        .order_by(Inventory.product_id)
    )

    inventory_list = db.scalars(statement).all()

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
        )
        for inventory in inventory_list
    ]

def get_inventory_by_id(db: Session, product_id: UUID):
    # Ambil inventory beserta relasi Product
    statement = (
        select(Inventory)
        .where(Inventory.product_id == product_id)
        .options(selectinload(Inventory.product))
    )

    get_inventory = db.scalar(statement)

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