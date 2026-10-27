from fastapi import status
from app.errors.base import AppError

class StockNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Stock not found"
    error_code = "PRODUCT_NOT_FOUND"

class InventoryNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Inventory not found"
    error_code = "INVENTORY_NOT_FOUND"

class BookingNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Booking not found"
    error_code = "BOOKING_NOT_FOUND"

class InsufficientQtyError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Insufficient stock"
    error_code = "INSUFFICIENT_STOCK"

class BookingCannotBeCancelledError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Cannot Cancelled Booking"
    error_code = "CANNOT_CANCELLED_BOOKING"

class BookingCannotBeConfirmedError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Cannot Confirmed Booking"
    error_code = "CANNOT_CONFIRMED_BOOKING"