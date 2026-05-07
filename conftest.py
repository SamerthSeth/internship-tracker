"""
Test configuration and fixtures
pytest configuration and test utilities
"""

import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.database import Base
from app.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_db():
    """Create a test database session"""
    # Use SQLite for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }


@pytest.fixture
def test_certificate_data():
    """Sample certificate data for testing"""
    from datetime import date
    return {
        "title": "Test Certificate",
        "platform": "Coursera",
        "category": "AI/ML",
        "description": "Test certificate description",
        "issue_date": date.today(),
        "expiry_date": None
    }


@pytest.fixture
def test_internship_data():
    """Sample internship data for testing"""
    from datetime import date
    return {
        "company": "Test Company",
        "role": "Test Role",
        "description": "Test internship description",
        "start_date": date.today(),
        "end_date": None,
        "is_ongoing": True
    }
