"""
Database seed script - Populate database with sample data
Run this after initializing the database to add sample data for testing
"""

import asyncio
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.models import UserModel, CertificateModel, InternshipModel
from app.core.security import hash_password


async def seed_database():
    """Seed database with sample data"""
    
    # Create engine and session
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        try:
            # Create sample users
            user1 = UserModel(
                email="john@example.com",
                username="john_dev",
                full_name="John Developer",
                hashed_password=hash_password("SecurePassword123!"),
                is_active=True
            )
            
            user2 = UserModel(
                email="jane@example.com",
                username="jane_coder",
                full_name="Jane Coder",
                hashed_password=hash_password("AnotherSecure456!"),
                is_active=True
            )
            
            session.add(user1)
            session.add(user2)
            await session.flush()
            
            # Create certificates for user1
            today = date.today()
            certificates = [
                CertificateModel(
                    user_id=user1.id,
                    title="AI and Machine Learning Fundamentals",
                    platform="Coursera",
                    category="AI/ML",
                    description="Comprehensive course on AI fundamentals and ML algorithms",
                    issue_date=today - timedelta(days=180),
                    expiry_date=today + timedelta(days=180),
                    is_expired=False
                ),
                CertificateModel(
                    user_id=user1.id,
                    title="Python for Data Science",
                    platform="Udacity",
                    category="Programming",
                    description="Professional certification in Python for data science",
                    issue_date=today - timedelta(days=120),
                    expiry_date=today + timedelta(days=240),
                    is_expired=False
                ),
                CertificateModel(
                    user_id=user1.id,
                    title="Deep Learning Specialization",
                    platform="Coursera",
                    category="AI/ML",
                    description="Advanced deep learning specialization with neural networks",
                    issue_date=today - timedelta(days=90),
                    expiry_date=today + timedelta(days=270),
                    is_expired=False
                ),
            ]
            
            session.add_all(certificates)
            
            # Create certificates for user2
            user2_certificates = [
                CertificateModel(
                    user_id=user2.id,
                    title="Cloud Computing Essentials",
                    platform="AWS",
                    category="Cloud",
                    description="AWS certified cloud practitioner",
                    issue_date=today - timedelta(days=100),
                    expiry_date=today + timedelta(days=260),
                    is_expired=False
                ),
            ]
            
            session.add_all(user2_certificates)
            await session.flush()
            
            # Create internships for user1
            internships = [
                InternshipModel(
                    user_id=user1.id,
                    company="TechCorp Inc",
                    role="Backend Engineer Intern",
                    description="Worked on building scalable REST APIs using Python and FastAPI",
                    start_date=today - timedelta(days=180),
                    end_date=today - timedelta(days=90),
                    is_ongoing=False
                ),
                InternshipModel(
                    user_id=user1.id,
                    company="AI Solutions Ltd",
                    role="Machine Learning Intern",
                    description="Developed ML models for predictive analytics",
                    start_date=today - timedelta(days=60),
                    end_date=today + timedelta(days=30),
                    is_ongoing=True
                ),
            ]
            
            session.add_all(internships)
            
            # Create internships for user2
            user2_internships = [
                InternshipModel(
                    user_id=user2.id,
                    company="CloudIT Solutions",
                    role="DevOps Intern",
                    description="Worked on CI/CD pipelines and infrastructure automation",
                    start_date=today - timedelta(days=150),
                    end_date=today - timedelta(days=30),
                    is_ongoing=False
                ),
                InternshipModel(
                    user_id=user2.id,
                    company="CloudIT Solutions",
                    role="DevOps Engineer",
                    description="Full-time position managing cloud infrastructure",
                    start_date=today - timedelta(days=20),
                    end_date=today + timedelta(days=100),
                    is_ongoing=True
                ),
            ]
            
            session.add_all(user2_internships)
            
            # Commit all changes
            await session.commit()
            
            print("✅ Database seeded successfully!")
            print(f"📊 Created {len(certificates) + len(user2_certificates)} certificates")
            print(f"💼 Created {len(internships) + len(user2_internships)} internships")
            print(f"👥 Created 2 users:")
            print(f"   - john@example.com (john_dev)")
            print(f"   - jane@example.com (jane_coder)")
            
        except Exception as e:
            print(f"❌ Error seeding database: {str(e)}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())
