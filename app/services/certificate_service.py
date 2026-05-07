"""
Certificate service - Business logic for certificate operations
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models import CertificateModel
from app.schemas import CertificateCreate, CertificateUpdate
from app.utils import file_manager
from app.utils.exceptions import NotFoundException
from app.utils.helpers import is_date_expired


class CertificateService:
    """Service for certificate operations"""
    
    @staticmethod
    async def create_certificate(
        db: AsyncSession,
        user_id: int,
        certificate: CertificateCreate,
        file_url: str = None
    ) -> CertificateModel:
        """
        Create new certificate
        
        Args:
            db: Database session
            user_id: User ID
            certificate: Certificate data
            file_url: File URL if uploaded
        
        Returns:
            Created certificate
        """
        is_expired = is_date_expired(certificate.expiry_date)
        
        db_certificate = CertificateModel(
            user_id=user_id,
            title=certificate.title,
            platform=certificate.platform,
            category=certificate.category,
            description=certificate.description,
            issue_date=certificate.issue_date,
            expiry_date=certificate.expiry_date,
            file_url=file_url,
            is_expired=is_expired,
        )
        db.add(db_certificate)
        await db.commit()
        await db.refresh(db_certificate)
        return db_certificate
    
    @staticmethod
    async def get_certificate_by_id(
        db: AsyncSession,
        certificate_id: int,
        user_id: int
    ) -> CertificateModel:
        """
        Get certificate by ID (belongs to user)
        
        Args:
            db: Database session
            certificate_id: Certificate ID
            user_id: User ID
        
        Returns:
            Certificate model
        
        Raises:
            NotFoundException: If certificate not found
            ForbiddenException: If certificate doesn't belong to user
        """
        result = await db.execute(
            select(CertificateModel).where(
                and_(
                    CertificateModel.id == certificate_id,
                    CertificateModel.user_id == user_id
                )
            )
        )
        certificate = result.scalar_one_or_none()
        
        if not certificate:
            raise NotFoundException("Certificate not found")
        
        return certificate
    
    @staticmethod
    async def get_user_certificates(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list:
        """
        Get all certificates for user
        
        Args:
            db: Database session
            user_id: User ID
            skip: Skip count
            limit: Limit count
        
        Returns:
            List of certificates
        """
        result = await db.execute(
            select(CertificateModel)
            .where(CertificateModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_certificate(
        db: AsyncSession,
        certificate_id: int,
        user_id: int,
        certificate_update: CertificateUpdate,
        file_url: str = None
    ) -> CertificateModel:
        """
        Update certificate
        
        Args:
            db: Database session
            certificate_id: Certificate ID
            user_id: User ID
            certificate_update: Update data
            file_url: New file URL if uploaded
        
        Returns:
            Updated certificate
        """
        certificate = await CertificateService.get_certificate_by_id(
            db, certificate_id, user_id
        )
        
        # Update fields
        update_data = certificate_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(certificate, field, value)
        
        # Update file URL if provided
        if file_url:
            if certificate.file_url:
                file_manager.delete_file(certificate.file_url)
            certificate.file_url = file_url
        
        # Update expiry status
        certificate.is_expired = is_date_expired(certificate.expiry_date)
        
        await db.commit()
        await db.refresh(certificate)
        return certificate
    
    @staticmethod
    async def delete_certificate(
        db: AsyncSession,
        certificate_id: int,
        user_id: int
    ) -> bool:
        """
        Delete certificate
        
        Args:
            db: Database session
            certificate_id: Certificate ID
            user_id: User ID
        
        Returns:
            True if deleted
        """
        certificate = await CertificateService.get_certificate_by_id(
            db, certificate_id, user_id
        )

        if certificate.file_url:
            file_manager.delete_file(certificate.file_url)
        
        await db.delete(certificate)
        await db.commit()
        return True
    
    @staticmethod
    async def get_expired_certificates(db: AsyncSession, user_id: int) -> list:
        """
        Get expired certificates for user
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            List of expired certificates
        """
        result = await db.execute(
            select(CertificateModel).where(
                and_(
                    CertificateModel.user_id == user_id,
                    CertificateModel.is_expired == True
                )
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_certificates_by_category(
        db: AsyncSession,
        user_id: int,
        category: str
    ) -> list:
        """
        Get certificates by category
        
        Args:
            db: Database session
            user_id: User ID
            category: Certificate category
        
        Returns:
            List of certificates in category
        """
        result = await db.execute(
            select(CertificateModel).where(
                and_(
                    CertificateModel.user_id == user_id,
                    CertificateModel.category == category
                )
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def count_ai_certificates(db: AsyncSession, user_id: int) -> int:
        """
        Count AI-related certificates for user
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            Count of AI certificates
        """
        result = await db.execute(
            select(CertificateModel).where(
                and_(
                    CertificateModel.user_id == user_id,
                    CertificateModel.category.ilike("%ai%")
                )
            )
        )
        return len(result.scalars().all())
