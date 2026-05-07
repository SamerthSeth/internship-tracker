"""
Certificate routes - CRUD operations for certificates
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db
from app.schemas import CertificateCreate, CertificateUpdate, CertificateResponse
from app.services import CertificateService
from app.utils import file_manager
from app.utils.exceptions import NotFoundException
from app.routes.auth import get_current_user

router = APIRouter(prefix="/certificates", tags=["Certificates"])
security = HTTPBearer()


@router.post("", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
async def create_certificate(
    certificate: CertificateCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new certificate
    
    Args:
        certificate: Certificate data
        credentials: JWT token
        db: Database session
    
    Returns:
        Created certificate
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    db_certificate = await CertificateService.create_certificate(
        db, user_id, certificate
    )
    
    return db_certificate


@router.post("/upload", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
async def create_certificate_with_file(
    title: str,
    platform: str,
    category: str,
    issue_date: str,
    file: UploadFile = File(...),
    description: str = None,
    expiry_date: str = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Create certificate with file upload
    
    Args:
        title: Certificate title
        platform: Platform name
        category: Certificate category
        issue_date: Issue date (YYYY-MM-DD)
        file: Certificate file to upload
        description: Certificate description
        expiry_date: Expiry date (YYYY-MM-DD)
        credentials: JWT token
        db: Database session
    
    Returns:
        Created certificate with file
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    # Save file
    file_path = await file_manager.save_file(file, subdirectory=f"certificates/{user_id}")
    
    # Create certificate
    certificate = CertificateCreate(
        title=title,
        platform=platform,
        category=category,
        issue_date=issue_date,  # Will be converted to date by Pydantic
        description=description,
        expiry_date=expiry_date,
    )
    
    db_certificate = await CertificateService.create_certificate(
        db, user_id, certificate, file_url=file_path
    )
    
    return db_certificate


@router.get("", response_model=list)
async def get_certificates(
    skip: int = 0,
    limit: int = 100,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all certificates for current user
    
    Args:
        skip: Skip count
        limit: Limit count
        credentials: JWT token
        db: Database session
    
    Returns:
        List of certificates
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    certificates = await CertificateService.get_user_certificates(
        db, user_id, skip, limit
    )
    
    return certificates


@router.get("/{certificate_id}", response_model=CertificateResponse)
async def get_certificate(
    certificate_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific certificate
    
    Args:
        certificate_id: Certificate ID
        credentials: JWT token
        db: Database session
    
    Returns:
        Certificate details
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    try:
        certificate = await CertificateService.get_certificate_by_id(
            db, certificate_id, user_id
        )
        return certificate
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{certificate_id}", response_model=CertificateResponse)
async def update_certificate(
    certificate_id: int,
    certificate_update: CertificateUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Update certificate
    
    Args:
        certificate_id: Certificate ID
        certificate_update: Update data
        credentials: JWT token
        db: Database session
    
    Returns:
        Updated certificate
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    try:
        certificate = await CertificateService.update_certificate(
            db, certificate_id, user_id, certificate_update
        )
        return certificate
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{certificate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certificate(
    certificate_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete certificate
    
    Args:
        certificate_id: Certificate ID
        credentials: JWT token
        db: Database session
    """
    user = get_current_user(credentials)
    user_id = user["user_id"]
    
    try:
        await CertificateService.delete_certificate(db, certificate_id, user_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
