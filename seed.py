import asyncio
import sys
import os

# Add the app directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core import async_session_maker
from app.services import UserService
from app.schemas import UserCreate

async def seed():
    async with async_session_maker() as session:
        try:
            user = UserCreate(email="login@gmail.com", password="123456", full_name="Test User")
            await UserService.create_user(session, user)
            print("Successfully created test user: login@gmail.com")
        except Exception as e:
            print(f"Error creating user (might already exist): {e}")

if __name__ == "__main__":
    asyncio.run(seed())
