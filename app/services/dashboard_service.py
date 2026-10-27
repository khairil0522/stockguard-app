from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.products import Product
from app.models.inventory import Inventory

def get_dashboard_stats(db: Session) -> dict:
    total_products = db.scalar(
        select(func.count())
        .select_from(Product)
        .where(Product.is_active.is_(True))
    ) or 0

    available_stock = db.scalar(
        select(
            func.coalesce(
                func.sum(Inventory.on_hand - Inventory.reserved_qty),
                0,
            )
        )
    ) or 0

    return {
        "total_products": total_products,
        "available_stock": available_stock,
    }