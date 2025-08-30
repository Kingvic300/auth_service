# Use official Python image as base
FROM python:3.11-slim

# Metadata
LABEL maintainer="DELL USER"

# Prevent Python from writing .pyc files & buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run entrypoint script (we’ll create this next)
ENTRYPOINT ["/app/entrypoint.sh"]
