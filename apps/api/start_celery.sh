#!/bin/bash
# Script pour démarrer Celery worker

echo "Démarrage du worker Celery..."
python -m celery -A app.workers.celery_app worker --loglevel=info


