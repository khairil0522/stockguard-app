from fastapi import FastAPI
from app.api.v1.root import router as root_router
from app.api.v1.products import router as products_router
from app.api.v1.stock_adjustments import router as stock_adjustments_router
from app.api.v1.booking import router as booking_router
from app.api.v1.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StockGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(products_router, prefix="/api/v1")
app.include_router(stock_adjustments_router, prefix="/api/v1")
app.include_router(booking_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")