#!/bin/bash
set -e

echo "=== CENet Backend Startup ==="
echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Starting application..."
gunicorn \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  main:app
