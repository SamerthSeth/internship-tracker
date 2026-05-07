"""
Dashboard and eligibility service - Dashboard stats and eligibility checking
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func
from sqlalchemy.future import select
from datetime import date, timedelta
from app.models import CertificateModel, InternshipModel
from app.schemas import (
    DashboardStats,
    UpcomingDeadline,
    EligibilityCheckResponse,
    EligibilityRequirement,
)
from app.utils.helpers import get_days_until_date


class DashboardService:
    """Service for dashboard statistics"""
    
    @staticmethod
    async def get_dashboard_stats(db: AsyncSession, user_id: int) -> DashboardStats:
        """
        Get dashboard statistics for user
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            Dashboard statistics
        """
        # Count total certificates
        cert_result = await db.execute(
            select(func.count(CertificateModel.id)).where(
                CertificateModel.user_id == user_id
            )
        )
        total_certificates = cert_result.scalar() or 0
        
        # Count active internships
        intern_result = await db.execute(
            select(func.count(InternshipModel.id)).where(
                and_(
                    InternshipModel.user_id == user_id,
                    InternshipModel.is_ongoing == True
                )
            )
        )
        active_internships = intern_result.scalar() or 0
        
        # Count expired certificates
        expired_result = await db.execute(
            select(func.count(CertificateModel.id)).where(
                and_(
                    CertificateModel.user_id == user_id,
                    CertificateModel.is_expired == True
                )
            )
        )
        expired_certificates = expired_result.scalar() or 0
        
        # Count upcoming deadlines (within 7 days)
        today = date.today()
        upcoming_date = today + timedelta(days=7)
        
        # Certificates expiring soon
        cert_upcoming = await db.execute(
            select(func.count(CertificateModel.id)).where(
                and_(
                    CertificateModel.user_id == user_id,
                    CertificateModel.expiry_date >= today,
                    CertificateModel.expiry_date <= upcoming_date,
                    CertificateModel.is_expired == False
                )
            )
        )
        cert_count = cert_upcoming.scalar() or 0
        
        # Internships ending soon
        intern_upcoming = await db.execute(
            select(func.count(InternshipModel.id)).where(
                and_(
                    InternshipModel.user_id == user_id,
                    InternshipModel.end_date >= today,
                    InternshipModel.end_date <= upcoming_date,
                    InternshipModel.is_ongoing == True
                )
            )
        )
        intern_count = intern_upcoming.scalar() or 0
        
        upcoming_deadlines = cert_count + intern_count
        
        return DashboardStats(
            total_certificates=total_certificates,
            active_internships=active_internships,
            expired_certificates=expired_certificates,
            upcoming_deadlines=upcoming_deadlines,
        )
    
    @staticmethod
    async def get_upcoming_deadlines(
        db: AsyncSession,
        user_id: int,
        days_threshold: int = 7
    ) -> list:
        """
        Get upcoming deadlines for user
        
        Args:
            db: Database session
            user_id: User ID
            days_threshold: Days to look ahead
        
        Returns:
            List of upcoming deadlines
        """
        today = date.today()
        upcoming_date = today + timedelta(days=days_threshold)
        deadlines = []
        
        # Get certificates expiring soon
        cert_result = await db.execute(
            select(CertificateModel).where(
                and_(
                    CertificateModel.user_id == user_id,
                    CertificateModel.expiry_date.is_not(None),
                    CertificateModel.expiry_date >= today,
                    CertificateModel.expiry_date <= upcoming_date,
                    CertificateModel.is_expired == False
                )
            )
        )
        
        for cert in cert_result.scalars().all():
            days_left = get_days_until_date(cert.expiry_date)
            deadlines.append(
                UpcomingDeadline(
                    id=cert.id,
                    title=cert.title,
                    type="certificate",
                    deadline_date=cert.expiry_date,
                    days_remaining=days_left,
                )
            )
        
        # Get internships ending soon
        intern_result = await db.execute(
            select(InternshipModel).where(
                and_(
                    InternshipModel.user_id == user_id,
                    InternshipModel.end_date.is_not(None),
                    InternshipModel.end_date >= today,
                    InternshipModel.end_date <= upcoming_date,
                    InternshipModel.is_ongoing == True
                )
            )
        )
        
        for intern in intern_result.scalars().all():
            days_left = get_days_until_date(intern.end_date)
            deadlines.append(
                UpcomingDeadline(
                    id=intern.id,
                    title=f"{intern.role} at {intern.company}",
                    type="internship",
                    deadline_date=intern.end_date,
                    days_remaining=days_left,
                )
            )
        
        # Sort by deadline date
        deadlines.sort(key=lambda x: x.deadline_date)
        return deadlines


class EligibilityService:
    """Service for eligibility checking"""
    
    @staticmethod
    async def check_eligibility(db: AsyncSession, user_id: int) -> EligibilityCheckResponse:
        """
        Check user eligibility based on requirements
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            Eligibility check response
        """
        requirements = []
        missing_requirements = []
        recommendations = []
        
        # Requirement 1: Minimum 2 internships
        internship_count = await db.execute(
            select(func.count(InternshipModel.id)).where(
                InternshipModel.user_id == user_id
            )
        )
        internship_total = internship_count.scalar() or 0
        internship_met = internship_total >= 2
        
        requirements.append(
            EligibilityRequirement(
                requirement="Minimum 2 internships",
                is_met=internship_met,
                current_count=internship_total,
                required_count=2,
                details=f"You have completed {internship_total} internships",
            )
        )
        
        if not internship_met:
            missing_requirements.append(f"Need {2 - internship_total} more internship(s)")
            recommendations.append(
                f"Complete {2 - internship_total} more internship(s) to meet requirements"
            )
        
        # Requirement 2: At least 1 AI-related certificate
        ai_result = await db.execute(
            select(func.count(CertificateModel.id)).where(
                and_(
                    CertificateModel.user_id == user_id,
                    CertificateModel.category.ilike("%ai%")
                )
            )
        )
        ai_cert_count = ai_result.scalar() or 0
        ai_met = ai_cert_count >= 1
        
        requirements.append(
            EligibilityRequirement(
                requirement="At least 1 AI-related certificate",
                is_met=ai_met,
                current_count=ai_cert_count,
                required_count=1,
                details=f"You have {ai_cert_count} AI-related certificate(s)",
            )
        )
        
        if not ai_met:
            missing_requirements.append("Need 1 AI-related certificate")
            recommendations.append(
                "Obtain a certificate in AI/Machine Learning from platforms like Coursera, udacity, or edX"
            )
        
        # Determine overall eligibility
        is_eligible = internship_met and ai_met
        
        return EligibilityCheckResponse(
            is_eligible=is_eligible,
            requirements=requirements,
            missing_requirements=missing_requirements,
            recommendations=recommendations if not is_eligible else None,
        )
