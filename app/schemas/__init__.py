"""
Schemas module initialization
"""

from app.schemas.schemas import (
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    TokenResponse,
    TokenRefreshRequest,
    CertificateBase,
    CertificateCreate,
    CertificateUpdate,
    CertificateResponse,
    InternshipBase,
    InternshipCreate,
    InternshipUpdate,
    InternshipResponse,
    DashboardStats,
    UpcomingDeadline,
    UpcomingDeadlinesResponse,
    EligibilityCheckResponse,
    EligibilityRequirement,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "TokenResponse",
    "TokenRefreshRequest",
    "CertificateBase",
    "CertificateCreate",
    "CertificateUpdate",
    "CertificateResponse",
    "InternshipBase",
    "InternshipCreate",
    "InternshipUpdate",
    "InternshipResponse",
    "DashboardStats",
    "UpcomingDeadline",
    "UpcomingDeadlinesResponse",
    "EligibilityCheckResponse",
    "EligibilityRequirement",
]
