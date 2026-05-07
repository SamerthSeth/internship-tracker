"""
User service - Business logic for user operations
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import UserModel
from app.schemas import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password
from app.utils.exceptions import DuplicateException, NotFoundException, UnauthorizedException


class UserService:
    """Service for user operations"""
    
    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate) -> UserModel:
        """
        Create new user
        
        Args:
            db: Database session
            user: User data
        
        Returns:
            Created user
        
        Raises:
            DuplicateException: If user with email exists
        """
        # Check if email exists
        result = await db.execute(
            select(UserModel).where(UserModel.email == user.email)
        )
        if result.scalar_one_or_none():
            raise DuplicateException("User with this email already exists")
        
        # Check if username exists
        result = await db.execute(
            select(UserModel).where(UserModel.username == user.username)
        )
        if result.scalar_one_or_none():
            raise DuplicateException("Username already taken")
        
        # Create user
        db_user = UserModel(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hash_password(user.password),
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> UserModel:
        """
        Get user by email
        
        Args:
            db: Database session
            email: User email
        
        Returns:
            User model
        
        Raises:
            NotFoundException: If user not found
        """
        result = await db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
        return user
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> UserModel:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            User model
        
        Raises:
            NotFoundException: If user not found
        """
        result = await db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
        return user
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserModel:
        """
        Authenticate user with email and password
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
        
        Returns:
            Authenticated user
        
        Raises:
            UnauthorizedException: If credentials invalid
        """
        user = await UserService.get_user_by_email(db, email)
        
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")
        
        if not user.is_active:
            raise UnauthorizedException("User account is inactive")
        
        return user
    
    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        user_update: UserUpdate
    ) -> UserModel:
        """
        Update user
        
        Args:
            db: Database session
            user_id: User ID
            user_update: Update data
        
        Returns:
            Updated user
        
        Raises:
            NotFoundException: If user not found
            DuplicateException: If email/username already exists
        """
        user = await UserService.get_user_by_id(db, user_id)
        
        # Check if new email is unique
        if user_update.email and user_update.email != user.email:
            result = await db.execute(
                select(UserModel).where(UserModel.email == user_update.email)
            )
            if result.scalar_one_or_none():
                raise DuplicateException("Email already in use")
        
        # Check if new username is unique
        if user_update.username and user_update.username != user.username:
            result = await db.execute(
                select(UserModel).where(UserModel.username == user_update.username)
            )
            if result.scalar_one_or_none():
                raise DuplicateException("Username already taken")
        
        # Update fields
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list:
        """
        Get all users with pagination
        
        Args:
            db: Database session
            skip: Skip count
            limit: Limit count
        
        Returns:
            List of users
        """
        result = await db.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        return result.scalars().all()
