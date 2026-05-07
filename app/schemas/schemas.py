"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime


# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for user update"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)


# ==================== Token Schemas ====================

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str


class TokenData(BaseModel):
    """Schema for decoded token data"""
    user_id: int
    email: str


# ==================== Certificate Schemas ====================

class CertificateBase(BaseModel):
    """Base certificate schema"""
    title: str = Field(..., min_length=3, max_length=255)
    platform: str = Field(..., min_length=2, max_length=255)
    category: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    issue_date: date
    expiry_date: Optional[date] = None


class CertificateCreate(CertificateBase):
    """Schema for certificate creation"""
    pass


class CertificateUpdate(BaseModel):
    """Schema for certificate update"""
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    platform: Optional[str] = Field(None, min_length=2, max_length=255)
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None


class CertificateResponse(CertificateBase):
    """Schema for certificate response"""
    id: int
    user_id: int
    file_url: Optional[str]
    is_expired: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CertificateWithFileResponse(CertificateResponse):
    """Certificate response with file upload support"""
    pass


# ==================== Internship Schemas ====================

class InternshipBase(BaseModel):
    """Base internship schema"""
    company: str = Field(..., min_length=2, max_length=255)
    role: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_ongoing: bool = True


class InternshipCreate(InternshipBase):
    """Schema for internship creation"""
    pass


class InternshipUpdate(BaseModel):
    """Schema for internship update"""
    company: Optional[str] = Field(None, min_length=2, max_length=255)
    role: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_ongoing: Optional[bool] = None


class InternshipResponse(InternshipBase):
    """Schema for internship response"""
    id: int
    user_id: int
    file_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Dashboard Schemas ====================

class DashboardStats(BaseModel):
    """Schema for dashboard statistics"""
    total_certificates: int = 0
    active_internships: int = 0
    expired_certificates: int = 0
    upcoming_deadlines: int = 0


class UpcomingDeadline(BaseModel):
    """Schema for upcoming deadline"""
    id: int
    title: str
    type: str  # "certificate" or "internship"
    deadline_date: date
    days_remaining: int


class UpcomingDeadlinesResponse(BaseModel):
    """Schema for upcoming deadlines response"""
    deadlines: List[UpcomingDeadline]


# ==================== Eligibility Check Schemas ====================

class EligibilityRequirement(BaseModel):
    """Schema for individual eligibility requirement"""
    requirement: str
    is_met: bool
    current_count: Optional[int] = None
    required_count: Optional[int] = None
    details: Optional[str] = None


class EligibilityCheckResponse(BaseModel):
    """Schema for eligibility check response"""
    is_eligible: bool
    requirements: List[EligibilityRequirement]
    missing_requirements: List[str] = []
    recommendations: Optional[List[str]] = None
