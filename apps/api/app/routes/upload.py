from __future__ import annotations

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import Job, JobStatus, User
from app.routes.auth import get_current_user

router = APIRouter()


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Validate file type
    if not file.filename.endswith(".zip"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only ZIP files are allowed",
        )
    
    # Create upload directory
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    job_id = str(uuid.uuid4())
    filename = f"{job_id}_{file.filename}"
    file_path = upload_dir / filename
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )
    
    # Create job record
    job = Job(
        user_id=current_user.id,
        status=JobStatus.PENDING.value,
        upload_path=str(file_path),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    return {"job_id": job.id, "message": "File uploaded successfully"}

