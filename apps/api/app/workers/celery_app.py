from __future__ import annotations

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "strava_saas",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Import tasks so Celery can discover them
    imports=("app.workers.visualization_job",),
    # Use solo pool on Windows (prefork doesn't work on Windows)
    task_always_eager=False,
    worker_pool="solo",  # Use solo pool on Windows
)

# Import tasks to register them
from app.workers import visualization_job  # noqa: E402, F401

