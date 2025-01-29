#!/bin/bash

# Wait for the backend to be ready
/app/entrypoint/wait-for-it.sh backend:8000

# Start the worker
celery -A config.celery_app worker --loglevel=info