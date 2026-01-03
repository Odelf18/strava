from __future__ import annotations

import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

from app.core.config import settings


class StorageManager:
    """Manage file storage with automatic cleanup."""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_output_zip(self, job_id: int, files: dict[str, str]) -> str:
        """Create a ZIP file containing all visualization outputs."""
        zip_path = self.output_dir / f"visualizations_{job_id}.zip"
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for viz_type, file_path in files.items():
                if Path(file_path).exists():
                    zipf.write(file_path, arcname=f"{viz_type}.png")
        
        return str(zip_path)
    
    def cleanup_old_files(self) -> None:
        """Remove files older than retention period."""
        cutoff_time = datetime.now() - timedelta(hours=settings.FILE_RETENTION_HOURS)
        
        # Cleanup uploads
        for file_path in self.upload_dir.iterdir():
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    file_path.unlink()
        
        # Cleanup outputs
        for file_path in self.output_dir.iterdir():
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    file_path.unlink()

