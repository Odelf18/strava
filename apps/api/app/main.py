from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine, init_db
from app.routes import auth, download, jobs, payment, upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Strava Visualization SaaS API",
    description="API for generating artistic Strava visualizations",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(payment.router, prefix="/api/payment", tags=["payment"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(download.router, prefix="/api/download", tags=["download"])


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

