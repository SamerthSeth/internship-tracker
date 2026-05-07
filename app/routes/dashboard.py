"""
Dashboard routes - Dashboard stats, deadlines, eligibility
"""

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.schemas import DashboardStats, UpcomingDeadlinesResponse, EligibilityCheckResponse
from app.services import DashboardService, EligibilityService
from app.routes.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
security = HTTPBearer()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get dashboard statistics for current user
    
    Args:
        credentials: JWT token
        db: Database session
    
    Returns:
        Dashboard statistics
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    stats = await DashboardService.get_dashboard_stats(db, user_id)
    return stats


@router.get("/upcoming-deadlines", response_model=UpcomingDeadlinesResponse)
async def get_upcoming_deadlines(
    days: int = 7,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get upcoming deadlines for current user
    
    Args:
        days: Number of days to look ahead (default: 7)
        credentials: JWT token
        db: Database session
    
    Returns:
        List of upcoming deadlines
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    deadlines = await DashboardService.get_upcoming_deadlines(db, user_id, days)
    return UpcomingDeadlinesResponse(deadlines=deadlines)


@router.get("/eligibility", response_model=EligibilityCheckResponse)
async def check_eligibility(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Check eligibility status for current user
    
    Requirements:
    - Minimum 2 internships
    - At least 1 AI-related certificate
    
    Args:
        credentials: JWT token
        db: Database session
    
    Returns:
        Eligibility check result
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    eligibility = await EligibilityService.check_eligibility(db, user_id)
    return eligibility
