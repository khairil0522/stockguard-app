from fastapi import status
from app.errors.base import AppError

class InventoryNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Inventory not found"
    error_code = "INVENTORY_NOT_FOUND"