"""
Internship routes - CRUD operations for internships
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.schemas import InternshipCreate, InternshipUpdate, InternshipResponse
from app.services import InternshipService
from app.utils import file_manager
from app.utils.exceptions import NotFoundException
from app.routes.auth import get_current_user

router = APIRouter(prefix="/internships", tags=["Internships"])
security = HTTPBearer()


@router.post("", response_model=InternshipResponse, status_code=status.HTTP_201_CREATED)
async def create_internship(
    internship: InternshipCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new internship
    
    Args:
        internship: Internship data
        credentials: JWT token
        db: Database session
    
    Returns:
        Created internship
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    db_internship = await InternshipService.create_internship(
        db, user_id, internship
    )
    
    return db_internship


@router.post("/upload", response_model=InternshipResponse, status_code=status.HTTP_201_CREATED)
async def create_internship_with_file(
    company: str,
    role: str,
    start_date: str,
    file: UploadFile = File(...),
    description: str = None,
    end_date: str = None,
    is_ongoing: bool = True,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Create internship with file upload
    
    Args:
        company: Company name
        role: Role/position
        start_date: Start date (YYYY-MM-DD)
        file: Internship certificate/proof file
        description: Internship description
        end_date: End date (YYYY-MM-DD)
        is_ongoing: Whether internship is ongoing
        credentials: JWT token
        db: Database session
    
    Returns:
        Created internship with file
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    # Save file
    file_path = await file_manager.save_file(file, subdirectory=f"internships/{user_id}")
    
    # Create internship
    internship = InternshipCreate(
        company=company,
        role=role,
        start_date=start_date,
        description=description,
        end_date=end_date,
        is_ongoing=is_ongoing,
    )
    
    db_internship = await InternshipService.create_internship(
        db, user_id, internship, file_url=file_path
    )
    
    return db_internship


@router.get("", response_model=list[InternshipResponse])
async def get_internships(
    skip: int = 0,
    limit: int = 100,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all internships for current user
    
    Args:
        skip: Skip count
        limit: Limit count
        credentials: JWT token
        db: Database session
    
    Returns:
        List of internships
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    internships = await InternshipService.get_user_internships(
        db, user_id, skip, limit
    )
    
    return internships


@router.get("/active", response_model=list[InternshipResponse])
async def get_active_internships(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get active internships for current user
    
    Args:
        credentials: JWT token
        db: Database session
    
    Returns:
        List of active internships
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    internships = await InternshipService.get_active_internships(db, user_id)
    
    return internships


@router.get("/{internship_id}", response_model=InternshipResponse)
async def get_internship(
    internship_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific internship
    
    Args:
        internship_id: Internship ID
        credentials: JWT token
        db: Database session
    
    Returns:
        Internship details
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    try:
        internship = await InternshipService.get_internship_by_id(
            db, internship_id, user_id
        )
        return internship
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{internship_id}", response_model=InternshipResponse)
async def update_internship(
    internship_id: int,
    internship_update: InternshipUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Update internship
    
    Args:
        internship_id: Internship ID
        internship_update: Update data
        credentials: JWT token
        db: Database session
    
    Returns:
        Updated internship
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    try:
        internship = await InternshipService.update_internship(
            db, internship_id, user_id, internship_update
        )
        return internship
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{internship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_internship(
    internship_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete internship
    
    Args:
        internship_id: Internship ID
        credentials: JWT token
        db: Database session
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    try:
        await InternshipService.delete_internship(db, internship_id, user_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
