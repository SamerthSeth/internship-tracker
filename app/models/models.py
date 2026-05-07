"""
Database models using SQLAlchemy ORM
Defines User, Certificate, and Internship entities with relationships
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Date, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class UserModel(Base):
    """User entity for authentication and profile"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    certificates = relationship("CertificateModel", back_populates="user", cascade="all, delete-orphan")
    internships = relationship("InternshipModel", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"


class CertificateModel(Base):
    """Certificate entity linking to users"""
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    platform = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    file_url = Column(String(500), nullable=True)
    is_expired = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("UserModel", back_populates="certificates")
    
    def __repr__(self):
        return f"<Certificate(id={self.id}, title='{self.title}', user_id={self.user_id})>"


class InternshipModel(Base):
    """Internship entity linking to users"""
    __tablename__ = "internships"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    company = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_ongoing = Column(Boolean, default=True)
    file_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("UserModel", back_populates="internships")
    
    def __repr__(self):
        return f"<Internship(id={self.id}, company='{self.company}', role='{self.role}', user_id={self.user_id})>"
