from fastapi import status
from app.errors.base import AppError

class ProductNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product not found"
    error_code = "PRODUCT_NOT_FOUND"

class DuplicateSKUError(AppError):
    status_code=status.HTTP_409_CONFLICT
    detail="SKU already exists"
    error_code = "SKU_ALREADY_EXISTS"

class ProductHasStockError(AppError):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Product has stock, cannot be deactivated"
    error_code = "PRODUCT_HAS_STOCK"

class ProductInactiveError(AppError):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Product is inactive"
    error_code = "PRODUCT_INACTIVE"