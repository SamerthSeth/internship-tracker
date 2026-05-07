"""
Internship service - Business logic for internship operations
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from datetime import date
from app.models import InternshipModel
from app.schemas import InternshipCreate, InternshipUpdate
from app.utils.exceptions import NotFoundException


class InternshipService:
    """Service for internship operations"""
    
    @staticmethod
    async def create_internship(
        db: AsyncSession,
        user_id: int,
        internship: InternshipCreate,
        file_url: str = None
    ) -> InternshipModel:
        """
        Create new internship
        
        Args:
            db: Database session
            user_id: User ID
            internship: Internship data
            file_url: File URL if uploaded
        
        Returns:
            Created internship
        """
        db_internship = InternshipModel(
            user_id=user_id,
            company=internship.company,
            role=internship.role,
            description=internship.description,
            start_date=internship.start_date,
            end_date=internship.end_date,
            is_ongoing=internship.is_ongoing,
            file_url=file_url,
        )
        db.add(db_internship)
        await db.commit()
        await db.refresh(db_internship)
        return db_internship
    
    @staticmethod
    async def get_internship_by_id(
        db: AsyncSession,
        internship_id: int,
        user_id: int
    ) -> InternshipModel:
        """
        Get internship by ID (belongs to user)
        
        Args:
            db: Database session
            internship_id: Internship ID
            user_id: User ID
        
        Returns:
            Internship model
        
        Raises:
            NotFoundException: If internship not found
        """
        result = await db.execute(
            select(InternshipModel).where(
                and_(
                    InternshipModel.id == internship_id,
                    InternshipModel.user_id == user_id
                )
            )
        )
        internship = result.scalar_one_or_none()
        
        if not internship:
            raise NotFoundException("Internship not found")
        
        return internship
    
    @staticmethod
    async def get_user_internships(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list:
        """
        Get all internships for user
        
        Args:
            db: Database session
            user_id: User ID
            skip: Skip count
            limit: Limit count
        
        Returns:
            List of internships
        """
        result = await db.execute(
            select(InternshipModel)
            .where(InternshipModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_active_internships(
        db: AsyncSession,
        user_id: int
    ) -> list:
        """
        Get active/ongoing internships for user
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            List of active internships
        """
        result = await db.execute(
            select(InternshipModel).where(
                and_(
                    InternshipModel.user_id == user_id,
                    InternshipModel.is_ongoing == True
                )
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def count_internships(db: AsyncSession, user_id: int) -> int:
        """
        Count total internships for user
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            Count of internships
        """
        result = await db.execute(
            select(InternshipModel).where(InternshipModel.user_id == user_id)
        )
        return len(result.scalars().all())
    
    @staticmethod
    async def update_internship(
        db: AsyncSession,
        internship_id: int,
        user_id: int,
        internship_update: InternshipUpdate,
        file_url: str = None
    ) -> InternshipModel:
        """
        Update internship
        
        Args:
            db: Database session
            internship_id: Internship ID
            user_id: User ID
            internship_update: Update data
            file_url: New file URL if uploaded
        
        Returns:
            Updated internship
        """
        internship = await InternshipService.get_internship_by_id(
            db, internship_id, user_id
        )
        
        # Update fields
        update_data = internship_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(internship, field, value)
        
        # Update file URL if provided
        if file_url:
            internship.file_url = file_url
        
        await db.commit()
        await db.refresh(internship)
        return internship
    
    @staticmethod
    async def delete_internship(
        db: AsyncSession,
        internship_id: int,
        user_id: int
    ) -> bool:
        """
        Delete internship
        
        Args:
            db: Database session
            internship_id: Internship ID
            user_id: User ID
        
        Returns:
            True if deleted
        """
        internship = await InternshipService.get_internship_by_id(
            db, internship_id, user_id
        )
        
        await db.delete(internship)
        await db.commit()
        return True
