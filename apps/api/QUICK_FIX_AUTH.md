# Fix rapide : "Could not validate credentials"

## Solution immédiate

Le problème vient probablement de la `SECRET_KEY` qui change à chaque redémarrage.

### 1. Créez un fichier `.env` dans `apps/api/`

```bash
cd apps/api
```

Créez le fichier `.env` avec ce contenu :

```env
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production-12345
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
DATABASE_URL=sqlite:///./strava_saas.db
```

**Important** : Utilisez une SECRET_KEY stable (ne changez pas cette valeur).

### 2. Redémarrez l'API

```bash
# Arrêtez l'API (Ctrl+C)
# Puis redémarrez :
python run.py
```

### 3. Reconnectez-vous

1. Allez sur http://localhost:3000/auth/login
2. Déconnectez-vous si vous êtes connecté
3. Reconnectez-vous avec votre email et mot de passe

Le nouveau token sera généré avec la SECRET_KEY stable.

## Vérification

Après connexion, vérifiez dans la console du navigateur (F12) :
```javascript
localStorage.getItem("token")
```

Le token devrait exister et être un long string commençant par `eyJ...`

## Si ça ne fonctionne toujours pas

1. **Supprimez l'ancien token** :
```javascript
localStorage.removeItem("token")
```

2. **Vérifiez les logs de l'API** - avec `DEBUG=True`, vous verrez des messages de débogage

3. **Testez directement avec curl** (voir `TEST_AUTH.md`)


