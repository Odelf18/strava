from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from app.core.config import settings
from app.core.database import SessionLocal
from app.models import Job, JobStatus
from app.services.extractor import ArchiveExtractor
from app.services.filter import DataFilter
from app.services.processor import VisualizationProcessor
from app.services.storage import StorageManager
from app.workers.celery_app import celery_app


def _process_job(job_id: int) -> None:
    """Internal function to process a visualization job."""
    db = SessionLocal()
    job = None
    
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return
        
        # Update status
        job.status = JobStatus.PROCESSING.value
        db.commit()
        
        # Extract archive
        extractor = ArchiveExtractor(
            zip_path=job.upload_path,
            extract_to=tempfile.mkdtemp(prefix=f"strava_extract_{job_id}_"),
        )
        archive_data = extractor.extract()
        
        if not archive_data["activities_dir"]:
            raise ValueError("No activities directory found in archive")
        
        # Parse filters
        filters = {}
        if job.sport_types:
            filters["sport_types"] = json.loads(job.sport_types)
        if job.date_from:
            filters["date_from"] = job.date_from
        if job.date_to:
            filters["date_to"] = job.date_to
        if job.bbox:
            filters["bbox"] = json.loads(job.bbox)
        if job.activity_ids:
            filters["activity_ids"] = json.loads(job.activity_ids)
        
        # Filter activities
        if archive_data["activities_data"] is not None:
            data_filter = DataFilter(
                activities_df=archive_data["activities_data"],
                activities_dir=archive_data["activities_dir"],
                **filters,
            )
            file_paths = data_filter.get_filtered_files()
            bbox_filter = data_filter.get_bbox_filter()
        else:
            # No activities.csv, process all files
            activities_dir = Path(archive_data["activities_dir"])
            file_paths = [
                str(f) for f in activities_dir.rglob("*")
                if f.suffix in [".fit", ".gpx", ".tcx"]
            ]
            bbox_filter = json.loads(job.bbox) if job.bbox else None
        
        if not file_paths:
            raise ValueError("No files to process after filtering")
        
        # Parse visualizations
        visualizations = json.loads(job.visualizations) if job.visualizations else ["all"]
        
        # Process visualizations
        processor = VisualizationProcessor(
            output_dir=tempfile.mkdtemp(prefix=f"strava_output_{job_id}_"),
        )
        
        outputs = processor.process(
            file_paths=file_paths,
            activities_csv=archive_data["activities_csv"],
            visualizations=visualizations,
            bbox=bbox_filter,
        )
        
        if not outputs:
            raise ValueError("No visualizations generated")
        
        # Create output ZIP
        storage = StorageManager()
        output_zip = storage.create_output_zip(job_id, outputs)
        
        # Update job
        job.output_path = output_zip
        job.status = JobStatus.COMPLETED.value
        from datetime import datetime
        job.completed_at = datetime.utcnow()
        db.commit()
        
        # Cleanup extracted files
        shutil.rmtree(archive_data["extract_path"], ignore_errors=True)
        shutil.rmtree(processor.output_dir, ignore_errors=True)
        
    except Exception as e:
        if job:
            job.status = JobStatus.FAILED.value
            job.error_message = str(e)
            db.commit()
        raise
    finally:
        db.close()


# Function that can be called directly (for testing without Celery)
def process_visualization_job(job_id: int) -> None:
    """Process a visualization job (can be called directly)."""
    _process_job(job_id)


# Celery task - must be registered with the correct name
@celery_app.task(bind=True, max_retries=3)
def process_visualization_job_task(self, job_id: int) -> None:
    """Celery task wrapper for process_visualization_job."""
    try:
        _process_job(job_id)
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
