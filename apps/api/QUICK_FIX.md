# Fix rapide CORS et erreur 500

## Étapes rapides

### 1. Arrêtez l'API (Ctrl+C dans le terminal)

### 2. Créez/éditez `.env` dans `apps/api/`

Créez le fichier `apps/api/.env` avec ce contenu :

```env
DEBUG=True
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///./strava_saas.db
```

### 3. Redémarrez l'API

```bash
cd apps/api
python run.py
```

Vous devriez voir :
```
✓ Database initialized successfully
✓ Temp directories created: ...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Testez dans le navigateur

Allez sur http://localhost:3000/auth/register et essayez de créer un compte.

## Si ça ne marche toujours pas

### Vérifiez les logs de l'API

Dans le terminal où l'API tourne, vous verrez l'erreur exacte. Les erreurs courantes :

1. **"No such table: users"** → La base n'est pas créée
   - Solution : Supprimez `strava_saas.db` et redémarrez l'API

2. **"email-validator not found"** → Dépendance manquante
   - Solution : `pip install email-validator`

3. **Erreur de connexion** → Vérifiez que l'API écoute sur le bon port
   - Solution : Vérifiez http://localhost:8000/api/health

## Test rapide avec curl

```bash
# Test health
curl http://localhost:8000/api/health

# Test register (devrait fonctionner maintenant)
curl -X POST http://localhost:8000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"test@test.com\", \"password\": \"test123\"}"
```


