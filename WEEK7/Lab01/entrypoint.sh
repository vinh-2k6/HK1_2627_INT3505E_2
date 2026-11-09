#!/bin/sh
set -e

echo "Applying database migrations..."
flask --app wsgi.py db upgrade || {
    echo "Running fallback database initialization..."
    python -c "from src.main import create_app; from src.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
}

echo "Starting Gunicorn server on 0.0.0.0:5000..."
exec gunicorn --bind 0.0.0.0:5000 "src.main:create_app()"
