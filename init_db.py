"""
Database initialization script
Initialize the database with table creation
"""

import asyncio
from app.core.database import init_db, drop_db


async def main():
    """Initialize database"""
    print("🔄 Initializing database...")
    
    try:
        # Uncomment the line below to drop all tables first (careful with production!)
        # await drop_db()
        # print("🗑️ Dropped all tables")
        
        await init_db()
        print("✅ Database initialized successfully!")
        print("💡 Run 'python seed_db.py' to populate with sample data")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
