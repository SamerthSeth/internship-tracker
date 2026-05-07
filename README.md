# Smart Internship & Certificate Tracker Backend

Production-ready FastAPI backend for managing internships and certificates.

## Features

- ✅ JWT-based authentication with access and refresh tokens
- ✅ User management (signup, login, profile)
- ✅ Certificate management (CRUD with file uploads)
- ✅ Internship management (CRUD with file uploads)
- ✅ Dashboard with statistics and upcoming deadlines
- ✅ Eligibility checker for program requirements
- ✅ Async/await support with SQLAlchemy
- ✅ PostgreSQL database with Alembic migrations
- ✅ Clean architecture with modular code structure
- ✅ Comprehensive error handling
- ✅ Swagger/OpenAPI documentation
- ✅ CORS support

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async)
- **Authentication**: JWT (python-jose)
- **Password**: bcrypt
- **Migrations**: Alembic
- **API Documentation**: Swagger/OpenAPI

## Project Structure

```
app/
├── main.py                 # FastAPI app entry point
├── core/                   # Core application modules
│   ├── config.py          # Configuration management
│   ├── database.py        # Database setup and session management
│   ├── security.py        # JWT and password utilities
│   └── __init__.py
├── models/                # SQLAlchemy ORM models
│   ├── models.py          # User, Certificate, Internship models
│   └── __init__.py
├── schemas/               # Pydantic request/response schemas
│   ├── schemas.py         # All request/response models
│   └── __init__.py
├── routes/                # API route handlers
│   ├── auth.py            # Authentication endpoints
│   ├── certificates.py    # Certificate CRUD endpoints
│   ├── internships.py     # Internship CRUD endpoints
│   ├── dashboard.py       # Dashboard and eligibility endpoints
│   └── __init__.py
├── services/              # Business logic layer
│   ├── user_service.py    # User operations
│   ├── certificate_service.py  # Certificate operations
│   ├── internship_service.py   # Internship operations
│   ├── dashboard_service.py    # Dashboard and eligibility logic
│   └── __init__.py
├── utils/                 # Utility functions
│   ├── file_upload.py     # File upload management
│   ├── exceptions.py      # Custom exceptions
│   ├── helpers.py         # Helper functions
│   └── __init__.py
└── __init__.py

alembic/                    # Database migrations
├── versions/              # Migration files
├── env.py                 # Alembic environment
└── script.py.mako         # Migration template

uploads/                    # File storage (user uploads)
.env                        # Environment variables (development)
.env.example               # Environment variables template
requirements.txt           # Python dependencies
init_db.py                 # Database initialization script
seed_db.py                 # Database seeding script
```

## Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or pipenv

### Installation Steps

1. **Clone or setup the project**
   ```bash
   cd tracker-project
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On Unix/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy .env.example to .env and update values
   cp .env.example .env
   ```

5. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb tracker_db
   
   # Update DATABASE_URL in .env with your credentials
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/tracker_db
   ```

6. **Initialize database**
   ```bash
   python init_db.py
   ```

7. **Seed sample data (optional)**
   ```bash
   python seed_db.py
   ```

8. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
- Swagger docs: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token

### Certificates
- `GET /certificates` - Get all certificates
- `GET /certificates/{id}` - Get certificate by ID
- `POST /certificates` - Create certificate
- `POST /certificates/upload` - Create certificate with file
- `PUT /certificates/{id}` - Update certificate
- `DELETE /certificates/{id}` - Delete certificate

### Internships
- `GET /internships` - Get all internships
- `GET /internships/active` - Get active internships
- `GET /internships/{id}` - Get internship by ID
- `POST /internships` - Create internship
- `POST /internships/upload` - Create internship with file
- `PUT /internships/{id}` - Update internship
- `DELETE /internships/{id}` - Delete internship

### Dashboard
- `GET /dashboard/stats` - Get dashboard statistics
- `GET /dashboard/upcoming-deadlines` - Get upcoming deadlines
- `GET /dashboard/eligibility` - Check eligibility status

## Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/tracker_db

# JWT
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
APP_NAME=Smart Internship & Certificate Tracker
DEBUG=True
ENVIRONMENT=development

# File Upload
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=pdf,jpg,jpeg,png
FILE_UPLOAD_DIRECTORY=uploads

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

## Database Migrations

Using Alembic for database version control:

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Signup/Login**: Get access and refresh tokens
2. **Access Token**: Use in `Authorization: Bearer <token>` header
3. **Refresh Token**: Use to get new access token when expired

Example:
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/certificates
```

## Error Handling

The API uses consistent error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common status codes:
- `200`: Success
- `201`: Created
- `204`: No Content (delete)
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict
- `422`: Validation Error
- `500`: Internal Server Error

## Production Deployment

1. **Update .env for production**
   ```env
   DEBUG=False
   ENVIRONMENT=production
   SECRET_KEY=<generate-strong-secret>
   CORS_ORIGINS=["https://yourdomain.com"]
   ```

2. **Use production server**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Database backups**
   ```bash
   pg_dump -U username tracker_db > backup.sql
   ```

## Contributing

Follow these guidelines:
- Use async/await for all database operations
- Add docstrings to all functions
- Handle exceptions appropriately
- Write tests for new features
- Follow PEP 8 style guide

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please create an issue in the repository.
