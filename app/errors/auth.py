from fastapi import status
from app.errors.base import AppError

class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"
    error_code = "UNAUTHORIZED"

class UserNotFoundError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "User not found"
    error_code = "USER_NOT_FOUND"

class InvalidUsernamePasswordError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid Username or Password"
    error_code = "INVALID_CREDENTIALS"

class TokenExpiredError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid Username or Password"
    error_code = "TOKEN_EXPIRED"

class PermissionDeniedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You do not have permission to perform this action."
    error = "PERMISSION_NOT_ALLOWED"