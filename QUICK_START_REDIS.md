# Démarrage rapide avec Redis

## Option la plus simple : Docker

Si vous avez Docker Desktop installé :

```bash
docker-compose up -d
```

Cela démarre Redis automatiquement. C'est tout !

## Vérifier que Redis fonctionne

```bash
# Test de connexion
python -c "import redis; r = redis.from_url('redis://localhost:6379/0'); print('Redis OK!' if r.ping() else 'Redis KO')"
```

## Alternative : Upstash (Cloud, gratuit)

1. Allez sur https://upstash.com
2. Créez un compte gratuit
3. Créez une base Redis
4. Copiez l'URL de connexion
5. Ajoutez-la dans `apps/api/.env` :

```
REDIS_URL=redis://default:VOTRE_PASSWORD@VOTRE_HOST:PORT
CELERY_BROKER_URL=redis://default:VOTRE_PASSWORD@VOTRE_HOST:PORT
CELERY_RESULT_BACKEND=redis://default:VOTRE_PASSWORD@VOTRE_HOST:PORT
```

## Démarrer l'application

Une fois Redis configuré :

**Terminal 1 - API:**
```bash
cd apps/api
python run.py
```

**Terminal 2 - Celery Worker:**

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

**Terminal 3 - Frontend:**
```bash
cd apps/web
npm run dev
```

## Pas de Docker ?

Voir `REDIS_WINDOWS_SETUP.md` pour d'autres options.

