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
    beat_schedule="app.workers.celery_beat_schedule.beat_schedule",
)

