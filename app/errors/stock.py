from fastapi import status
from app.errors.base import AppError

class StockNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Stock not found"
    error_code = "STOCK_NOT_FOUND"

class InsufficientStockError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Insufficient stock"
    error_code = "INSUFFICIENT_STOCK"