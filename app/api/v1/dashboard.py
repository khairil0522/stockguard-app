from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.dashboard import DashboardStatsResponse
from app.services.dashboard_service import get_dashboard_stats

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.get("/stats",response_model=DashboardStatsResponse)
def dashboard_stats(db: Session = Depends(get_db)):
    return get_dashboard_stats(db)