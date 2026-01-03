# Strava Visualization SaaS - Frontend

Next.js frontend with shadcn/ui for the Strava visualization SaaS platform.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start development server:
```bash
npm run dev
```

## Pages

- `/` - Homepage
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/dashboard` - User dashboard with jobs
- `/upload` - Upload Strava ZIP file
- `/configure/[jobId]` - Configure visualizations and filters before payment

## Features

- Modern UI with shadcn/ui components
- JWT authentication
- File upload with progress
- Configuration interface for visualizations and filters
- Stripe Checkout integration
- Download results


