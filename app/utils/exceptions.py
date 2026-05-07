"""
Exception handling utilities
Custom exceptions and error responses
"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class BaseAppException(HTTPException):
    """Base exception for application"""
    
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UnauthorizedException(BaseAppException):
    """Raised when user is not authorized"""
    
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(BaseAppException):
    """Raised when user doesn't have permission"""
    
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class NotFoundException(BaseAppException):
    """Raised when resource is not found"""
    
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ValidationException(BaseAppException):
    """Raised when validation fails"""
    
    def __init__(self, detail: str = "Validation error"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class DuplicateException(BaseAppException):
    """Raised when duplicate resource exists"""
    
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class ConflictException(BaseAppException):
    """Raised on conflicting operations"""
    
    def __init__(self, detail: str = "Operation conflict"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)
