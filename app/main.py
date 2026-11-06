from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #antisipasi supaya tidak CORS
from app.api.v1.root import router as root_router
from app.api.v1.router import router as api_v1_router

app = FastAPI(title="StockGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"], #daftarkan alamatnya di sini
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(api_v1_router, prefix="/api/v1")