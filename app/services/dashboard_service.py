from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dashboard_repository import dashboard_repository


class DashboardService:
    async def get_dashboard_stats(self, db: AsyncSession) -> dict:
        total_products = (await dashboard_repository.count_active_products(db))

        available_stock = (await dashboard_repository.get_available_stock(db))

        return {
            "total_products": total_products,
            "available_stock": available_stock,
        }

dashboard_service = DashboardService()