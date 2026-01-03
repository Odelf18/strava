# Comment démarrer l'API

## Prérequis

1. **Python 3.10+** installé
2. **Redis** en cours d'exécution (pour Celery)
3. **Dépendances** installées

## Installation des dépendances

Si ce n'est pas déjà fait :

```bash
cd apps/api
pip install -r requirements.txt
```

## Configuration

Créez un fichier `.env` dans `apps/api/` :

```env
DEBUG=True
SECRET_KEY=ma-cle-secrete-stable-ne-changez-pas
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
DATABASE_URL=sqlite:///./strava_saas.db
UPLOAD_DIR=./temp/uploads
OUTPUT_DIR=./temp/outputs
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Démarrer l'API

### Option 1 : Avec le script Python

```bash
cd apps/api
python run.py
```

### Option 2 : Avec uvicorn directement

```bash
cd apps/api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : **http://localhost:8000**

## Démarrer le worker Celery (optionnel mais recommandé)

Dans un **nouveau terminal** :

```bash
cd apps/api
python -m celery -A app.workers.celery_app worker --loglevel=info --pool=solo
```

Ou utilisez le script :
```bash
start_celery.bat
```

## Vérification

Une fois démarré, vous devriez voir :
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ Database initialized successfully
✓ Temp directories created: ./temp/uploads, ./temp/outputs
```

Testez l'API : http://localhost:8000/api/health

## Ordre de démarrage recommandé

1. **Redis** (si pas déjà démarré)
   ```bash
   # Avec Docker :
   docker-compose up -d
   
   # Ou utilisez un service Redis cloud (Upstash, etc.)
   ```

2. **API FastAPI**
   ```bash
   cd apps/api
   python run.py
   ```

3. **Worker Celery** (dans un autre terminal)
   ```bash
   cd apps/api
   python -m celery -A app.workers.celery_app worker --loglevel=info --pool=solo
   ```

## Problèmes courants

### Erreur : "Module not found"
→ Installez les dépendances : `pip install -r requirements.txt`

### Erreur : "Redis connection refused"
→ Démarrez Redis ou configurez une URL Redis valide dans `.env`

### Erreur : "Port 8000 already in use"
→ Changez le port dans `run.py` ou arrêtez le processus qui utilise le port 8000

### Erreur : "Database not found"
→ L'API créera automatiquement la base de données SQLite au premier démarrage

## Documentation API

Une fois démarré, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

