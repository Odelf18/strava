# Installation Guide

## Prérequis

- Python 3.10+
- Node.js 18+
- Redis (pour Celery)
- Git

## Installation complète

### 1. Installer stravavis (package de base)

Depuis la racine du projet :

```bash
# À la racine (strava_py/)
pip install -e .
```

Cela installe le package `stravavis` avec toutes ses dépendances (matplotlib, pandas, gpxpy, etc.)

### 2. Installer les dépendances de l'API

```bash
cd apps/api
pip install -r requirements.txt
```

Cela installe FastAPI, Celery, Stripe, SQLAlchemy, etc.

### 3. Installer les dépendances du frontend

```bash
cd ../web
npm install
```

### 4. Configuration

#### Backend

Créez `.env` dans `apps/api/` :

```bash
cd apps/api
cp .env.example .env
# Éditez .env avec vos configurations
```

Variables importantes :
- `SECRET_KEY` : Générez une clé secrète (ex: `openssl rand -hex 32`)
- `DATABASE_URL` : SQLite pour dev (`sqlite:///./strava_saas.db`) ou PostgreSQL pour prod
- `STRIPE_SECRET_KEY` : Votre clé Stripe
- `STRIPE_WEBHOOK_SECRET` : Secret du webhook Stripe

#### Frontend

Créez `.env.local` dans `apps/web/` :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Démarrer les services

#### Terminal 1 : Redis
```bash
redis-server
```

#### Terminal 2 : API FastAPI
```bash
cd apps/api
python run.py
```

#### Terminal 3 : Worker Celery

**Windows:**
```bash
cd apps/api
python -m celery -A app.workers.celery_app worker --loglevel=info
```

**Mac/Linux:**
```bash
cd apps/api
celery -A app.workers.celery_app worker --loglevel=info
```

#### Terminal 4 : Frontend Next.js
```bash
cd apps/web
npm run dev
```

## Vérification

- API : http://localhost:8000/api/health
- Frontend : http://localhost:3000
- Docs API : http://localhost:8000/docs

## Dépannage

### Erreur "stravavis not found"

Assurez-vous d'avoir installé stravavis depuis la racine :
```bash
cd ../..
pip install -e .
```

### Erreur "Redis connection refused"

Démarrez Redis :
```bash
redis-server
```

Ou installez Redis si ce n'est pas fait :
- Windows : Téléchargez depuis https://github.com/microsoftarchive/redis/releases
- Mac : `brew install redis`
- Linux : `sudo apt-get install redis-server`

### Erreur de base de données

Pour SQLite (développement), la base est créée automatiquement au premier lancement.

Pour PostgreSQL (production), créez la base et mettez à jour `DATABASE_URL`.

