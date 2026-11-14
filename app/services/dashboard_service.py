from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Product
from app.models.inventory import Inventory

class DashboardService:
    async def get_dashboard_stats(self, db: AsyncSession) -> dict:
        total_products = await db.scalar(
            select(func.count())
            .select_from(Product)
            .where(Product.is_active.is_(True))
        ) or 0

        available_stock = await db.scalar(
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

dashboard_service = DashboardService()