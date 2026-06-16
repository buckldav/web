# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Don't buffer stdout/stderr so logs appear immediately
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies first (layer-cached until requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY main.py .

# Expose the port uvicorn will listen on
EXPOSE 8000

# Run with uvicorn directly (no --reload in production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
