#!/bin/bash

# Run Alembic migrations
# echo "Running Alembic migrations..."
alembic upgrade head

# Start FastAPI with Uvicorn
echo "Starting FastAPI application with Uvicorn..."
uvicorn main:app --host 0.0.0.0 --port 8000
