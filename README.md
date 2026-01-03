# Strava Visualization SaaS

A modern SaaS platform for creating artistic visualizations from Strava data.

## Features

- 🎨 **Multiple Visualization Types**: Maps, calendars, elevation profiles, facets, landscape, dumbbell plots
- 🚴 **Multi-Sport Support**: Works with all Strava activities (cycling, running, swimming, etc.)
- 🔍 **Advanced Filtering**: Filter by sport type, date range, geographic bounds, or specific activities
- 💳 **Stripe Integration**: Multiple pricing tiers with secure payment processing
- ⚡ **Async Processing**: Background job processing with Celery
- 📦 **Easy Upload**: Simply upload your Strava export ZIP file

## Architecture

This is a monorepo containing:

- **apps/api**: FastAPI backend with Celery workers
- **apps/web**: Next.js frontend with shadcn/ui
- **src/stravavis**: Core visualization library (enhanced with TCX support)

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis (for Celery)
- PostgreSQL (for production) or SQLite (for development)

### Backend Setup

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

4. Start Redis:
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

### Frontend Setup

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

## Pricing

- **$2**: Single visualization (no filters)
- **$3**: Single visualization (with filters)
- **$9.9**: All visualizations pack (no filters)
- **$19.9**: Premium pack (5 generations with custom filters)

## Development

### Project Structure

```
strava_py/
├── apps/
│   ├── api/          # FastAPI backend
│   └── web/            # Next.js frontend
├── packages/
│   └── shared/         # Shared TypeScript types
├── src/
│   └── stravavis/      # Core visualization library
└── tests/              # Tests
```

### Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Celery, Redis, Stripe
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- **Visualization**: matplotlib, plotnine, pandas, gpxpy, fit2gpx

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

Recommended setup:
- **Frontend**: Vercel
- **Backend**: Heroku or Railway
- **Database**: PostgreSQL (Heroku Postgres or Supabase)
- **Redis**: Heroku Redis or Upstash

## License

MIT

## Credits

Based on the original [strava_py](https://github.com/marcusvolz/strava_py) by Marcus Volz, enhanced for SaaS deployment.
