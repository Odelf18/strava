# Deployment Guide

## Recommended Deployment Strategy

### Frontend (Next.js)
**Platform**: Vercel (recommended) or Netlify

1. Connect your GitHub repository
2. Set build command: `cd apps/web && npm install && npm run build`
3. Set output directory: `apps/web/.next`
4. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-api-url.com`

### Backend API (FastAPI)
**Platform**: Heroku, Railway, or Render

#### Heroku Setup:
1. Create two apps: one for API, one for worker
2. Add PostgreSQL addon
3. Add Redis addon (Heroku Redis)
4. Set environment variables in Heroku dashboard
5. Deploy API app
6. Deploy worker with: `celery -A app.workers.celery_app worker --loglevel=info`

#### Railway Setup:
1. Create new project
2. Add PostgreSQL service
3. Add Redis service (Upstash)
4. Deploy API service
5. Add worker service with same codebase but different start command

### Environment Variables

#### Backend:
```
SECRET_KEY=<generate-secure-key>
DATABASE_URL=<postgres-connection-string>
REDIS_URL=<redis-connection-string>
CELERY_BROKER_URL=<redis-connection-string>
CELERY_RESULT_BACKEND=<redis-connection-string>
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
CORS_ORIGINS=["https://your-frontend-url.com"]
```

#### Frontend:
```
NEXT_PUBLIC_API_URL=https://your-api-url.com
```

### Stripe Webhook Setup

1. Go to Stripe Dashboard > Webhooks
2. Add endpoint: `https://your-api-url.com/api/payment/webhook`
3. Select events: `checkout.session.completed`
4. Copy webhook signing secret to `STRIPE_WEBHOOK_SECRET`

### Database Migrations

Run migrations on first deploy:
```bash
python -c "from app.core.database import init_db; init_db()"
```

Or use Alembic for production:
```bash
alembic upgrade head
```

### Monitoring

- Set up error tracking (Sentry recommended)
- Monitor Celery worker logs
- Set up uptime monitoring
- Monitor file storage usage

