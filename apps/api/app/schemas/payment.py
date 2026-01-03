from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel


class BoundingBox(BaseModel):
    lon_min: float
    lon_max: float
    lat_min: float
    lat_max: float


class Filters(BaseModel):
    sport_types: list[str] | None = None
    date_from: date | None = None
    date_to: date | None = None
    bbox: BoundingBox | None = None
    activity_ids: list[int] | None = None


class PaymentIntentCreate(BaseModel):
    job_id: int
    pack_type: Literal["single", "all", "premium"]
    visualization_type: str | None = None  # For single pack
    visualizations: list[str]  # List of visualization types
    has_filters: bool = False
    filters: Filters | None = None
    success_url: str
    cancel_url: str


class PaymentIntentResponse(BaseModel):
    checkout_url: str
    session_id: str

