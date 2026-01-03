from __future__ import annotations

from celery.schedules import crontab

# Celery beat schedule for periodic tasks
beat_schedule = {
    "cleanup-old-files": {
        "task": "app.workers.cleanup_job.cleanup_task",
        "schedule": crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
}

