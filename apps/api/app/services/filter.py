from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd


class DataFilter:
    """Filter activities based on various criteria."""
    
    def __init__(
        self,
        activities_df: pd.DataFrame,
        activities_dir: str,
        sport_types: list[str] | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        bbox: dict[str, float] | None = None,
        activity_ids: list[int] | None = None,
    ):
        self.activities_df = activities_df
        self.activities_dir = Path(activities_dir)
        self.sport_types = sport_types
        self.date_from = date_from
        self.date_to = date_to
        self.bbox = bbox
        self.activity_ids = activity_ids
    
    def filter_activities(self) -> pd.DataFrame:
        """Filter activities DataFrame based on criteria."""
        df = self.activities_df.copy()
        
        # Filter by sport type
        if self.sport_types:
            df = df[df["activity_type"].isin(self.sport_types)]
        
        # Filter by date range
        if "activity_date" in df.columns:
            if self.date_from:
                df = df[pd.to_datetime(df["activity_date"]) >= pd.Timestamp(self.date_from)]
            if self.date_to:
                df = df[pd.to_datetime(df["activity_date"]) <= pd.Timestamp(self.date_to)]
        
        # Filter by activity IDs
        if self.activity_ids:
            df = df[df["activity_id"].isin(self.activity_ids)]
        
        return df
    
    def get_filtered_files(self) -> list[str]:
        """Get list of file paths to process based on filters."""
        filtered_df = self.filter_activities()
        
        if filtered_df.empty:
            return []
        
        # Map activity IDs to files
        files = []
        for _, row in filtered_df.iterrows():
            filename = row.get("filename", "")
            if not filename:
                # Try to construct filename from activity_id
                activity_id = row.get("activity_id")
                if activity_id:
                    # Look for files matching the activity ID
                    pattern = f"*{activity_id}*"
                    matches = list(self.activities_dir.rglob(pattern))
                    if matches:
                        files.append(str(matches[0]))
                    continue
            
            # Handle relative paths
            if filename.startswith("activities/"):
                file_path = self.activities_dir.parent / filename
            else:
                file_path = self.activities_dir / filename
            
            # Try different extensions
            for ext in [".fit", ".gpx", ".tcx"]:
                test_path = file_path.with_suffix(ext)
                if test_path.exists():
                    files.append(str(test_path))
                    break
                # Also try without extension
                test_path = Path(str(file_path).replace(ext, ""))
                if test_path.exists():
                    files.append(str(test_path))
                    break
        
        return list(set(files))  # Remove duplicates
    
    def get_bbox_filter(self) -> dict[str, float] | None:
        """Return bbox filter for processing."""
        return self.bbox

