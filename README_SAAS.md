# Strava Visualization SaaS

A modern SaaS platform for creating artistic visualizations from Strava data.

## Architecture

This is a monorepo containing:

- **apps/api**: FastAPI backend with Celery workers
- **apps/web**: Next.js frontend with shadcn/ui
- **src/stravavis**: Core visualization library (enhanced)

## Quick Start

### Backend (API)

1. Navigate to `apps/api`:
```bash
cd apps/api
```

2. Install dependencies:
```bash
pip install -e .
```

3. Setup environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start Redis (required for Celery):
```bash
redis-server
```

5. Start the API:
```bash
python run.py
```

6. Start Celery worker (in separate terminal):
```bash
celery -A app.workers.celery_app worker --loglevel=info
```

### Frontend (Web)

1. Navigate to `apps/web`:
```bash
cd apps/web
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start development server:
```bash
npm run dev
```

## Features

- **Authentication**: Email/password with JWT
- **File Upload**: Strava export ZIP files
- **Filtering**: Sport type, date range, geographic bounds, activity selection
- **Visualizations**: Maps, calendars, elevation profiles, facets, landscape, dumbbell
- **Payment**: Stripe integration with multiple pricing tiers
- **Background Processing**: Celery workers for async job processing
- **File Management**: Automatic cleanup after 24 hours

## Pricing

- **$2**: Single visualization (no filters)
- **$3**: Single visualization (with filters)
- **$9.9**: All visualizations pack (no filters)
- **$19.9**: Premium pack (5 generations with custom filters)

## Deployment

### Recommended Setup

- **Frontend**: Vercel (free tier)
- **Backend API**: Heroku or Railway
- **Celery Worker**: Heroku worker dyno or Railway worker
- **Redis**: Heroku Redis addon or Upstash
- **Database**: PostgreSQL (Heroku Postgres or Supabase)

### Environment Variables

#### Backend (.env)
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-api-url.com
```

## Development

The project uses:
- **Python 3.10+** for backend
- **Node.js 18+** for frontend
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components

## License

MIT

