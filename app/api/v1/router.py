from fastapi import APIRouter

from app.api.v1.products import router as products_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.stock_adjustments import router as stock_adjustments_router
from app.api.v1.booking import router as booking_router
from app.api.v1.dashboard import router as dashboard_router

router = APIRouter()

router.include_router(products_router)
router.include_router(stock_adjustments_router)
router.include_router(booking_router)
router.include_router(dashboard_router)
router.include_router(inventory_router)