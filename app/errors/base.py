from fastapi import status

class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"
    error_code = "INTERNAL_SERVER_ERROR"

    def __init__(self, message: str | None = None):
        self.message = message or type(self).message
        super().__init__(self.message)