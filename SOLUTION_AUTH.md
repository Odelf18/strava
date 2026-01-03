# Solution au problème "Could not validate credentials"

## Le problème

L'erreur vient du fait que la `SECRET_KEY` change à chaque redémarrage de l'API si le fichier `.env` n'existe pas. Quand la SECRET_KEY change, tous les tokens JWT existants deviennent invalides.

## Solution en 3 étapes

### Étape 1 : Créer le fichier `.env`

Dans `apps/api/`, créez un fichier `.env` :

```bash
cd apps/api
```

Copiez ce contenu dans `.env` :

```env
DEBUG=True
SECRET_KEY=ma-cle-secrete-stable-123456789
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
DATABASE_URL=sqlite:///./strava_saas.db
```

**⚠️ IMPORTANT** : La SECRET_KEY doit être stable (ne pas changer). Pour générer une clé sécurisée :

```python
import secrets
print(secrets.token_urlsafe(32))
```

### Étape 2 : Redémarrer l'API

```bash
# Arrêtez l'API (Ctrl+C dans le terminal)
# Puis redémarrez :
python run.py
```

### Étape 3 : Se reconnecter

1. Allez sur http://localhost:3000
2. Cliquez sur "Logout" si vous êtes connecté
3. Reconnectez-vous avec votre email et mot de passe

Le nouveau token sera valide car il utilise la SECRET_KEY stable.

## Vérification

Après connexion, le dashboard devrait fonctionner et vous ne devriez plus voir d'erreur 401.

## Pourquoi ça arrive ?

- Sans `.env`, FastAPI utilise la valeur par défaut de `SECRET_KEY` dans le code
- Si le code change ou si l'API redémarre, la clé peut changer
- Les tokens JWT sont signés avec la SECRET_KEY, donc si elle change, les tokens deviennent invalides

## Prévention

Toujours utiliser un fichier `.env` avec une SECRET_KEY stable en production !


