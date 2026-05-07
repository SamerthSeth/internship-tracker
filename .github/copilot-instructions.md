<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Smart Internship & Certificate Tracker Backend - Development Guide

## Overview

This is a production-ready FastAPI backend for managing internships and certificates. The project follows clean architecture principles with separation of concerns, async/await support, and comprehensive error handling.

## Architecture

The application is organized into layers:

1. **Routes Layer** (`app/routes/`) - HTTP request handlers
2. **Services Layer** (`app/services/`) - Business logic
3. **Models Layer** (`app/models/`) - Database entities (SQLAlchemy ORM)
4. **Schemas Layer** (`app/schemas/`) - Pydantic validation models
5. **Core Layer** (`app/core/`) - Configuration, database, security
6. **Utils Layer** (`app/utils/`) - Helpers and exceptions

## Key Technologies

- **FastAPI** - Modern async web framework
- **SQLAlchemy** - Async ORM for database operations
- **PostgreSQL** - Primary database
- **JWT** - Token-based authentication
- **Alembic** - Database migrations

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` file with database credentials
3. Initialize database: `python init_db.py`
4. Seed sample data: `python seed_db.py`
5. Run server: `python -m uvicorn app.main:app --reload`

## API Documentation

Access Swagger UI at http://localhost:8000/api/docs

## Development Workflow

### Adding a New Feature

1. **Update Models** if needed in `app/models/models.py`
2. **Create Pydantic Schemas** in `app/schemas/schemas.py`
3. **Add Business Logic** in `app/services/`
4. **Create Routes** in `app/routes/`
5. **Test via API docs**

### Database Migrations

Use Alembic for schema changes:
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Code Style

- Use docstrings for all functions and classes
- Follow PEP 8 conventions
- Use type hints throughout
- Use async/await for I/O operations

## Authentication

JWT tokens are required for protected endpoints. Include in headers:
```
Authorization: Bearer <access_token>
```

## Testing

The application includes sample data in `seed_db.py` for testing:
- User: john@example.com / jane@example.com
- Multiple certificates and internships for testing

## Common Tasks

### Reset Database
```python
# In Python shell or script
import asyncio
from app.core import drop_db, init_db

asyncio.run(drop_db())
asyncio.run(init_db())
```

### Add New Environment Variable
1. Add to `.env` and `.env.example`
2. Add to `app/core/config.py` Settings class
3. Use via `settings.VARIABLE_NAME`

### Create New API Endpoint
1. Create route in appropriate `app/routes/` file
2. Use dependency injection for database session
3. Use HTTPBearer for JWT authentication
4. Return appropriate Pydantic schema
5. Include docstring with description

## Production Checklist

- [ ] Update SECRET_KEY to strong random value
- [ ] Set DEBUG=False
- [ ] Update CORS_ORIGINS for your domain
- [ ] Use production PostgreSQL database
- [ ] Set up database backups
- [ ] Use production ASGI server (Gunicorn/Uvicorn)
- [ ] Enable HTTPS
- [ ] Set up monitoring and logging
- [ ] Run database migrations
