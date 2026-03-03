FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=/app

# System dependencies required for:
# - unstructured
# - OpenCV (libGL)
# - PDF parsing
# - OCR
RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic-dev \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    tesseract-ocr \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==2.3.2

WORKDIR /app

# Copy dependency files first (better layer caching)
COPY pyproject.toml poetry.lock ./

# Install production dependencies
RUN poetry install --no-root --only main

# Copy source code
COPY . .

EXPOSE 8000

# IMPORTANT: Your FastAPI app lives in src/server.py
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]