# Guide de Dépannage

## Erreurs courantes et solutions

### 1. `ModuleNotFoundError: No module named 'email_validator'`

**Solution :**
```bash
pip install email-validator
```

Ou installez toutes les dépendances :
```bash
cd apps/api
pip install -r requirements.txt
```

### 2. `ImportError: stravavis not found`

**Solution :**
Installez stravavis depuis la racine du projet :
```bash
# À la racine (strava_py/)
pip install -e .
```

### 3. Redis connection errors

**Solutions :**
- Utilisez Docker : `docker-compose up -d`
- Ou utilisez Upstash (cloud) : https://upstash.com
- Voir `REDIS_WINDOWS_SETUP.md` pour plus d'options

### 4. `sqlalchemy.exc.OperationalError: no such table: users`

**Solution :**
La base de données n'est pas initialisée. L'API crée automatiquement les tables au premier démarrage, mais si ça échoue :

```python
# Dans Python
from app.core.database import init_db
init_db()
```

### 5. `FileNotFoundError: .env`

**Solution :**
Créez le fichier `.env` dans `apps/api/` :
```bash
cd apps/api
cp .env.example .env
# Éditez .env avec vos configurations
```

### 6. Port 8000 déjà utilisé

**Solution :**
Changez le port dans `apps/api/run.py` :
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

### 7. CORS errors dans le frontend

**Solution :**
Ajoutez l'URL du frontend dans `apps/api/.env` :
```
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

### 8. Celery worker ne démarre pas

**Vérifications :**
1. Redis est-il démarré ? (`redis-cli ping` devrait retourner `PONG`)
2. Les variables d'environnement sont-elles correctes ?
3. Le worker est-il lancé depuis `apps/api/` ?

### 9. Erreurs de traitement de fichiers

**Vérifications :**
1. Les dossiers `temp/uploads` et `temp/outputs` existent-ils ?
2. Y a-t-il assez d'espace disque ?
3. Les fichiers ZIP sont-ils valides ?

### 10. Stripe webhook ne fonctionne pas

**Vérifications :**
1. `STRIPE_WEBHOOK_SECRET` est-il configuré dans `.env` ?
2. L'URL du webhook dans Stripe correspond-elle à votre API ?
3. Le webhook écoute-t-il l'événement `checkout.session.completed` ?

## Vérification de l'installation

Testez que tout est installé correctement :

```python
# Test Python
python -c "import stravavis; print('✓ stravavis OK')"
python -c "import app; print('✓ app OK')"
python -c "import redis; r = redis.from_url('redis://localhost:6379/0'); print('✓ Redis OK' if r.ping() else '✗ Redis KO')"
```

## Logs utiles

### API
Les logs de l'API apparaissent dans le terminal où vous avez lancé `python run.py`.

### Celery
Les logs du worker apparaissent dans le terminal où vous avez lancé `celery -A app.workers.celery_app worker`.

### Frontend
Les logs apparaissent dans le terminal où vous avez lancé `npm run dev` et dans la console du navigateur (F12).

## Obtenir de l'aide

1. Vérifiez les logs d'erreur dans les terminaux
2. Vérifiez que toutes les dépendances sont installées
3. Vérifiez les fichiers de configuration (`.env`, `.env.local`)
4. Consultez la documentation dans les fichiers README


