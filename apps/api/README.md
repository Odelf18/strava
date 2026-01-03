# Strava Visualization SaaS API

FastAPI backend for the Strava visualization SaaS platform.

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

3. Run database migrations (creates tables):
```bash
python -m app.main
```

4. Start Redis (required for Celery):
```bash
redis-server
```

5. Start the API:
```bash
uvicorn app.main:app --reload
```

6. Start Celery worker (in separate terminal):
```bash
celery -A app.workers.celery_app worker --loglevel=info
```

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `POST /api/upload` - Upload Strava ZIP file
- `POST /api/payment/create-checkout` - Create Stripe checkout session
- `POST /api/payment/webhook` - Stripe webhook handler
- `GET /api/jobs/{job_id}` - Get job status
- `GET /api/jobs/` - List user jobs
- `GET /api/download/{job_id}` - Download results

