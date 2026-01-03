from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class JobResponse(BaseModel):
    id: int
    status: str
    visualizations: str | None
    has_filters: bool
    created_at: datetime
    completed_at: datetime | None
    error_message: str | None
    
    class Config:
        from_attributes = True

