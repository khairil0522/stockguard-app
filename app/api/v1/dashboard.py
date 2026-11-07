from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.dashboard import DashboardStatsResponse
from app.services.dashboard_service import get_dashboard_stats

from app.dependencies.auth import require_permission

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.get("/stats",response_model=DashboardStatsResponse, 
            dependencies=[Depends(require_permission("dashboard.read"))],)
async def dashboard_stats(db: AsyncSession = Depends(get_db)):
    return await get_dashboard_stats(db)