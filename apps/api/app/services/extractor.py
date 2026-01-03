from __future__ import annotations

import gzip
import shutil
import zipfile
from pathlib import Path
from typing import Any

import pandas as pd


class ArchiveExtractor:
    """Extract and validate Strava export ZIP files."""
    
    def __init__(self, zip_path: str, extract_to: str):
        self.zip_path = Path(zip_path)
        self.extract_to = Path(extract_to)
        self.extract_to.mkdir(parents=True, exist_ok=True)
    
    def extract(self) -> dict[str, Any]:
        """Extract ZIP and return metadata about the archive."""
        with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
            zip_ref.extractall(self.extract_to)
        
        # Decompress .gz files
        self._decompress_gz_files(self.extract_to)
        
        # Find activities.csv
        activities_csv = self.extract_to / "activities.csv"
        if not activities_csv.exists():
            # Try to find it in subdirectories
            activities_csv = next(self.extract_to.rglob("activities.csv"), None)
        
        activities_data = None
        if activities_csv and activities_csv.exists():
            activities_data = self._parse_activities_csv(activities_csv)
        
        # Find activities directory
        activities_dir = self.extract_to / "activities"
        if not activities_dir.exists():
            activities_dir = next(self.extract_to.rglob("activities"), None)
        
        return {
            "activities_csv": str(activities_csv) if activities_csv else None,
            "activities_dir": str(activities_dir) if activities_dir else None,
            "activities_data": activities_data,
            "extract_path": str(self.extract_to),
        }
    
    def _decompress_gz_files(self, directory: Path) -> None:
        """Recursively decompress all .gz files in directory."""
        for gz_file in directory.rglob("*.gz"):
            output_file = gz_file.with_suffix("")
            if not output_file.exists():
                try:
                    with gzip.open(gz_file, "rb") as f_in:
                        with open(output_file, "wb") as f_out:
                            shutil.copyfileobj(f_in, f_out)
                except Exception as e:
                    print(f"Warning: Failed to decompress {gz_file}: {e}")
    
    def _parse_activities_csv(self, csv_path: Path) -> pd.DataFrame | None:
        """Parse activities.csv with locale detection."""
        try:
            # Try reading with different encodings
            for encoding in ["utf-8", "latin-1", "cp1252"]:
                try:
                    df = pd.read_csv(csv_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                return None
            
            # Normalize column names (handle French/English)
            column_mapping = {
                "ID de l'activité": "activity_id",
                "Activity ID": "activity_id",
                "Type d'activité": "activity_type",
                "Activity Type": "activity_type",
                "Date de l'activité": "activity_date",
                "Activity Date": "activity_date",
                "Nom du fichier": "filename",
                "Filename": "filename",
            }
            
            df = df.rename(columns=column_mapping)
            
            # Ensure required columns exist
            required_cols = ["activity_id", "activity_type", "activity_date"]
            if not all(col in df.columns for col in required_cols):
                # Try to find similar columns
                for req_col in required_cols:
                    if req_col not in df.columns:
                        # Look for similar column names
                        for col in df.columns:
                            if req_col.split("_")[0].lower() in col.lower():
                                df = df.rename(columns={col: req_col})
                                break
            
            return df
        except Exception as e:
            print(f"Error parsing activities.csv: {e}")
            return None

