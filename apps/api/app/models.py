from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    jobs = relationship("Job", back_populates="user")


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default=JobStatus.PENDING.value, nullable=False)
    payment_intent_id = Column(String, nullable=True)
    stripe_session_id = Column(String, nullable=True)
    
    # Configuration
    visualizations = Column(Text)  # JSON array of visualization types
    has_filters = Column(Boolean, default=False)
    sport_types = Column(Text, nullable=True)  # JSON array
    date_from = Column(DateTime, nullable=True)
    date_to = Column(DateTime, nullable=True)
    bbox = Column(Text, nullable=True)  # JSON: {lon_min, lon_max, lat_min, lat_max}
    activity_ids = Column(Text, nullable=True)  # JSON array
    
    # File paths
    upload_path = Column(String, nullable=True)
    output_path = Column(String, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="jobs")

