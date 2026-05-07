"""
Authentication routes - Signup, login, token refresh
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core import get_db, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.schemas import UserCreate, UserLogin, TokenResponse, TokenRefreshRequest
from app.services import UserService
from app.utils.exceptions import UnauthorizedException, DuplicateException

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register new user
    
    Args:
        user: User registration data
        db: Database session
    
    Returns:
        Access and refresh tokens
    """
    try:
        db_user = await UserService.create_user(db, user)
        
        # Create tokens
        access_token = create_access_token(
            {"user_id": db_user.id, "email": db_user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_refresh_token(
            {"user_id": db_user.id, "email": db_user.email}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except DuplicateException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Login user with email and password
    
    Args:
        credentials: Email and password
        db: Database session
    
    Returns:
        Access and refresh tokens
    """
    try:
        user = await UserService.authenticate_user(db, credentials.email, credentials.password)
        
        # Create tokens
        access_token = create_access_token(
            {"user_id": user.id, "email": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_refresh_token(
            {"user_id": user.id, "email": user.email}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    """
    Refresh access token using refresh token
    
    Args:
        request: Refresh token request
        db: Database session
    
    Returns:
        New access and refresh tokens
    """
    token_data = decode_token(request.refresh_token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user_id = token_data.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token data"
        )
    
    try:
        user = await UserService.get_user_by_id(db, user_id)
        
        # Create new tokens
        access_token = create_access_token(
            {"user_id": user.id, "email": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_refresh_token(
            {"user_id": user.id, "email": user.email}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_current_user(token: str = None):
    """
    Dependency to get current user from JWT token
    
    Args:
        token: JWT token from Authorization header
    
    Returns:
        User ID and email
    
    Raises:
        HTTPException: If token invalid or missing
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token"
        )
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    token_data = decode_token(token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = token_data.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token data"
        )
    
    return {"user_id": user_id, "email": token_data.get("email")}
