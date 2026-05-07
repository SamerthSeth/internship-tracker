"""
FastAPI application entry point
Main application with CORS, event handlers, and routes
"""

import os
import sys
from contextlib import asynccontextmanager

# Add project root to sys.path for direct script execution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core import init_db, engine, settings
from app.routes import auth, certificates, internships, dashboard

# Resolve runtime directories from project root for reliable serverless paths
UPLOADS_DIR = os.path.join(ROOT_DIR, "uploads")
STATIC_DIR = os.path.join(ROOT_DIR, "static")
os.makedirs(UPLOADS_DIR, exist_ok=True)

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

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# Mount static files for frontend
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    
    Returns:
        API information
    """
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
    }


# Serve frontend dashboard
@app.get("/dashboard", tags=["Frontend"])
async def dashboard_page():
    """
    Serve the frontend dashboard HTML page
    
    Returns:
        HTML dashboard page
    """
    dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "index.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"error": "Dashboard not found", "path": dashboard_path, "exists": os.path.exists(dashboard_path), "cwd": os.getcwd()}


# Debug: list all registered routes (temporary)
@app.get("/_routes", tags=["Debug"])
async def _list_routes():
    """Return registered routes for debugging"""
    routes = []
    for r in app.routes:
        path = getattr(r, "path", None) or getattr(r, "prefix", None) or str(r)
        methods = list(getattr(r, "methods", [])) if hasattr(r, "methods") else []
        routes.append({"path": path, "methods": methods})
    return routes


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        reload=False,
        log_level="info",
    )

