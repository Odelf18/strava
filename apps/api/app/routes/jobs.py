from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Job, JobStatus, User
from app.routes.auth import get_current_user
from app.schemas.job import JobResponse
from app.schemas.payment import PaymentIntentCreate

router = APIRouter()


@router.post("/{job_id}/configure")
async def configure_job(
    job_id: int,
    config_data: PaymentIntentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Configure and start processing a job (TEST MODE - no payment)."""
    # Validate job exists and belongs to user
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    if job.status != JobStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job is not in pending status. Current status: {job.status}",
        )
    
    # Update job configuration
    job.visualizations = json.dumps(config_data.visualizations)
    job.has_filters = config_data.has_filters and config_data.filters is not None
    
    if config_data.filters:
        if config_data.filters.sport_types:
            job.sport_types = json.dumps(config_data.filters.sport_types)
        if config_data.filters.date_from:
            job.date_from = config_data.filters.date_from
        if config_data.filters.date_to:
            job.date_to = config_data.filters.date_to
        if config_data.filters.bbox:
            job.bbox = json.dumps(config_data.filters.bbox.dict())
        if config_data.filters.activity_ids:
            job.activity_ids = json.dumps(config_data.filters.activity_ids)
    
    # Start processing immediately (TEST MODE - skip payment)
    job.status = JobStatus.PROCESSING.value
    db.commit()
    
    # Trigger processing (try Celery, fallback to sync if not available)
    try:
        from app.workers.visualization_job import process_visualization_job_task
        # Try to use Celery if available
        process_visualization_job_task.delay(job_id)
    except Exception as e:
        # If Celery is not available, process synchronously
        from app.workers.visualization_job import process_visualization_job
        try:
            # Process directly (for testing without Celery)
            process_visualization_job(job_id)
        except Exception as proc_error:
            job.status = JobStatus.FAILED.value
            job.error_message = str(proc_error)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start processing: {str(proc_error)}",
            )
    
    return {"message": "Job processing started", "job_id": job_id}


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return JobResponse.model_validate(job)


@router.get("/", response_model=list[JobResponse])
async def list_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    jobs = db.query(Job).filter(Job.user_id == current_user.id).offset(skip).limit(limit).all()
    return [JobResponse.model_validate(job) for job in jobs]
