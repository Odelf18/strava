from __future__ import annotations

from app.core.cleanup import cleanup_old_files
from app.workers.celery_app import celery_app


@celery_app.task
def cleanup_task():
    """Periodic task to cleanup old files."""
    cleanup_old_files()

