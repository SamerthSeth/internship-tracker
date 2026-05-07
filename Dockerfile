"""
Docker configuration for containerized deployment
"""

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (gcc for compiling packages, curl for health check)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY api/ ./api/
COPY static/ ./static/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY init_db.py .
COPY seed_db.py .
COPY vercel.json .

# Create uploads directory
RUN mkdir -p uploads

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
