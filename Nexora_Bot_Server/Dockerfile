# FROM python:3.11-slim

# ENV PYTHONUNBUFFERED=1 \
#     POETRY_VIRTUALENVS_CREATE=false \
#     POETRY_NO_INTERACTION=1 \
#     PYTHONPATH=/app


# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libmagic-dev \
#     libgl1 \
#     libglib2.0-0 \
#     poppler-utils \
#     tesseract-ocr \
#     libreoffice \
#     libreoffice-impress \
#     libreoffice-writer \
#     libreoffice-calc \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir poetry==2.3.2

# WORKDIR /app

# COPY pyproject.toml poetry.lock ./

# RUN poetry install --no-root --only main

# COPY . .

# EXPOSE 8000

# CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic-dev \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    libreoffice-impress \
    libreoffice-writer \
    libreoffice-calc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==2.3.2

# Copy dependency files first for caching
COPY pyproject.toml poetry.lock ./

# Install Python dependencies without cache
RUN poetry config cache-dir /tmp/poetry-cache \
    && poetry install --only main --no-root --no-interaction \
    && rm -rf /tmp/poetry-cache

# Copy application code
COPY src ./src
COPY supabase ./supabase

EXPOSE 8000

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]