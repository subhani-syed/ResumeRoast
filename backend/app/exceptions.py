from fastapi import HTTPException, status

class AuthException(HTTPException):
    """Base class for auth-related HTTP errors."""

    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class InvalidCredentials(AuthException):
    def __init__(self, detail: str = "Incorrect email or password"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class NotAuthenticated(AuthException):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class PermissionDenied(AuthException):
    def __init__(self, detail: str = "You do not have permission to access this resource"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)
