"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core import engine, init_db, settings
from app.routes import auth, certificates, dashboard, internships

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST_DIR = ROOT_DIR / "frontend" / "dist"
LEGACY_STATIC_DIR = ROOT_DIR / "static"

uploads_dir = Path(settings.FILE_UPLOAD_DIRECTORY)
if not uploads_dir.is_absolute():
    uploads_dir = ROOT_DIR / uploads_dir
uploads_dir.mkdir(parents=True, exist_ok=True)

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    print("Starting up the application...")
    try:
        await init_db()
        app.state.db_ready = True
        print("Database initialized")
    except Exception as exc:
        app.state.db_ready = False
        print(f"Database initialization failed: {exc}")
    yield
    # Shutdown
    print("Shutting down the application...")
    try:
        await engine.dispose()
        print("Database connections closed")
    except Exception as exc:
        print(f"Database shutdown cleanup failed: {exc}")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready API for Smart Internship & Certificate Tracker",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(certificates.router, prefix="/api")
app.include_router(internships.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "database_ready": bool(getattr(app.state, "db_ready", False)),
        "app": settings.APP_NAME,
        "version": "1.0.0"
    }


def _frontend_index_path() -> Path | None:
    """Return the best available frontend index path."""
    dist_index = FRONTEND_DIST_DIR / "index.html"
    if dist_index.exists():
        return dist_index
    legacy_index = LEGACY_STATIC_DIR / "index.html"
    if legacy_index.exists():
        return legacy_index
    return None


@app.get("/", include_in_schema=False)
async def root():
    """Serve frontend index when available, otherwise API metadata."""
    index_path = _frontend_index_path()
    if index_path:
        return FileResponse(index_path)
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
    }


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    """
    Serve frontend static files and SPA routes for non-API paths.
    """
    if (
        full_path == "health"
        or full_path.startswith("health/")
        or full_path.startswith(("api/", "uploads/"))
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    if FRONTEND_DIST_DIR.exists():
        requested_file = (FRONTEND_DIST_DIR / full_path).resolve()
        if (
            FRONTEND_DIST_DIR.resolve() in requested_file.parents
            and requested_file.exists()
            and requested_file.is_file()
        ):
            return FileResponse(requested_file)

    index_path = _frontend_index_path()
    if index_path:
        return FileResponse(index_path)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

