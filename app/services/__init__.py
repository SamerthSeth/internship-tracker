"""
Services module initialization
"""

from app.services.user_service import UserService
from app.services.certificate_service import CertificateService
from app.services.internship_service import InternshipService
from app.services.dashboard_service import DashboardService, EligibilityService

__all__ = [
    "UserService",
    "CertificateService",
    "InternshipService",
    "DashboardService",
    "EligibilityService",
]
