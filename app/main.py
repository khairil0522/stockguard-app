from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware #antisipasi supaya tidak CORS
from app.api.v1.root import router as root_router
from app.api.v1.router import router as api_v1_router

from app.errors.auth import PermissionDeniedError
from contextlib import asynccontextmanager
from app.scheduler.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()

    yield

app = FastAPI(
    title="StockGuard API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"], #daftarkan alamatnya di sini
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(api_v1_router, prefix="/api/v1")


@app.exception_handler(PermissionDeniedError)
async def permission_denied_handler(
    request: Request,
    exc: PermissionDeniedError,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error": exc.error,
        },
    )