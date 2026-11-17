from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory import Inventory
from app.models.products import Product


class DashboardRepository:

    async def count_active_products(self, db: AsyncSession) -> int:

        return (
            await db.scalar(
                select(func.count())
                .select_from(Product)
                .where(
                    Product.is_active.is_(True)
                )
            )
            or 0
        )

    async def get_available_stock(self, db: AsyncSession) -> int:

        return (
            await db.scalar(
                select(
                    func.coalesce(
                        func.sum(
                            Inventory.on_hand - Inventory.reserved_qty
                        ),
                        0,
                    )
                )
            )
            or 0
        )


dashboard_repository = DashboardRepository()