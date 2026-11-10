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

# Role Error List
class RoleNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Role not found"
    error_code = "ROLE_NOT_FOUND"

class RoleAlreadyError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Role has been already Used"
    error_code = "ROLE_ALREADY_USED"

class RoleAlreadyAssignedError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Role has been already Assigned"
    error_code = "ROLE_ALREADY_ASSIGNED"

class RoleProtectedError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Role Protected cannot be deleted"
    error_code = "ROLE_PROTECTED"

class RoleNotAllowDoubleError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Role System cannot be duplicated"
    error_code = "ROLE_DUPLICATED"

# Permission Error List
class PermissionNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Permission not found"
    error_code = "PERMISSION_NOT_FOUND"

class PermissionAlreadyError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Permission has been already Used"
    error_code = "PERMISSION_ALREADY_USED"

# Credential RBAC Error
class ProtectedRoleError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Role is Default System. Cannot be deleted"
    error_code = "ROLE_CANNOT_DELETE"

class UsernameAlreadyUsedError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "User has been already used"
    error_code = "USER_ALREADY_USED"

class EmailAlreadyUsedError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Email has been already used"
    error_code = "Email_ALREADY_USED"

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