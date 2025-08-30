#!/bin/sh

# Exit on error
set -e

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn --bind 0.0.0.0:8000 auth_service.wsgi:application
