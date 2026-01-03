from __future__ import annotations

import json

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import Job, JobStatus, User
from app.routes.auth import get_current_user
from app.schemas.payment import PaymentIntentCreate, PaymentIntentResponse

router = APIRouter()

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/create-checkout", response_model=PaymentIntentResponse)
async def create_checkout_session(
    payment_data: PaymentIntentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Validate job exists and belongs to user
    job = db.query(Job).filter(Job.id == payment_data.job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    if job.status != JobStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job is not in pending status",
        )
    
    # Calculate price
    if payment_data.pack_type == "premium":
        amount = settings.PRICE_PACK_PREMIUM
        description = "Premium Pack - 5 generations with filters"
    elif payment_data.pack_type == "all":
        amount = settings.PRICE_PACK_ALL
        description = "All Visualizations Pack"
    else:
        # Single visualization
        amount = settings.PRICE_SINGLE_WITH_FILTER if payment_data.has_filters else settings.PRICE_SINGLE_NO_FILTER
        description = f"Single Visualization ({payment_data.visualization_type})"
    
    # Create Stripe Checkout Session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Strava Visualization",
                            "description": description,
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{payment_data.success_url}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=payment_data.cancel_url,
            metadata={
                "job_id": str(job.id),
                "user_id": str(current_user.id),
                "pack_type": payment_data.pack_type,
                "visualization_type": payment_data.visualization_type or "",
                "has_filters": str(payment_data.has_filters),
            },
        )
        
        # Update job with payment info
        job.stripe_session_id = checkout_session.id
        job.visualizations = json.dumps(payment_data.visualizations)
        job.has_filters = payment_data.has_filters
        if payment_data.filters:
            if payment_data.filters.sport_types:
                job.sport_types = json.dumps(payment_data.filters.sport_types)
            if payment_data.filters.date_from:
                job.date_from = payment_data.filters.date_from
            if payment_data.filters.date_to:
                job.date_to = payment_data.filters.date_to
            if payment_data.filters.bbox:
                job.bbox = json.dumps(payment_data.filters.bbox.dict())
            if payment_data.filters.activity_ids:
                job.activity_ids = json.dumps(payment_data.filters.activity_ids)
        db.commit()
        
        return PaymentIntentResponse(checkout_url=checkout_session.url, session_id=checkout_session.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create checkout session: {str(e)}",
        )


@router.post("/webhook")
async def stripe_webhook(request: Request):
    import json
    
    # Get raw body (required for Stripe signature verification)
    body = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")
    
    try:
        event = stripe.Webhook.construct_event(
            body, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        job_id = int(session["metadata"]["job_id"])
        
        # Update job and trigger processing
        from app.core.database import SessionLocal
        db = SessionLocal()
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            if job:
                job.payment_intent_id = session.get("payment_intent")
                job.status = JobStatus.PROCESSING.value
                db.commit()
                
                # Trigger Celery task
                from app.workers.visualization_job import process_visualization_job_task
                process_visualization_job_task.delay(job_id)
        finally:
            db.close()
    
    return {"status": "success"}
