"""Quick seed script for creating a single login user."""

import asyncio

from app.core.database import AsyncSessionLocal, init_db
from app.schemas import UserCreate
from app.services import UserService
from app.utils.exceptions import DuplicateException


async def seed() -> None:
    """Create a default development user if it does not already exist."""
    await init_db()
    async with AsyncSessionLocal() as session:
        user = UserCreate(
            email="login@gmail.com",
            username="login_user",
            password="12345678",
            full_name="Test User",
        )
        try:
            await UserService.create_user(session, user)
            print("Created user login@gmail.com / 12345678")
        except DuplicateException:
            print("User login@gmail.com already exists")


if __name__ == "__main__":
    asyncio.run(seed())
