"""
Docker configuration for containerized deployment
"""

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy configuration and application code
COPY .env .
COPY app/ ./app/
COPY static/ ./static/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY init_db.py .
COPY seed_db.py .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
