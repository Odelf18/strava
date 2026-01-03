# Fix problème d'authentification "Could not validate credentials"

## Problème

L'erreur "Could not validate credentials" apparaît même après connexion.

## Causes possibles

1. **Token expiré** - Le token JWT a expiré (24h par défaut)
2. **SECRET_KEY différent** - Si l'API redémarre avec une nouvelle SECRET_KEY, les anciens tokens ne fonctionnent plus
3. **Token mal formaté** - Le token n'est pas correctement stocké ou envoyé
4. **Problème de timezone** - Les dates d'expiration peuvent être incorrectes

## Solutions

### 1. Vérifier le token dans le navigateur

Ouvrez la console du navigateur (F12) et tapez :
```javascript
localStorage.getItem("token")
```

Vérifiez que le token existe et n'est pas `null`.

### 2. Se reconnecter

Le token a peut-être expiré. Déconnectez-vous et reconnectez-vous :
1. Cliquez sur "Logout"
2. Reconnectez-vous avec votre email et mot de passe

### 3. Vérifier la SECRET_KEY

Assurez-vous que la `SECRET_KEY` dans `.env` est stable (ne change pas à chaque redémarrage) :

```env
SECRET_KEY=your-stable-secret-key-here
```

**Important** : Si vous changez la SECRET_KEY, tous les tokens existants deviendront invalides.

### 4. Vérifier les logs de l'API

Avec `DEBUG=True`, l'API affichera des messages de débogage dans le terminal :
- "No token provided"
- "Failed to decode token"
- "No 'sub' in payload"
- "User not found with id: X"

### 5. Test rapide

Testez l'authentification directement :

```bash
# 1. Se connecter
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@test.com&password=password123"

# Vous recevrez un token, copiez-le

# 2. Tester avec le token
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

### 6. Nettoyer et recommencer

Si rien ne fonctionne :

1. Supprimez le token du localStorage :
```javascript
localStorage.removeItem("token")
```

2. Supprimez la base de données (si en développement) :
```bash
rm apps/api/strava_saas.db
```

3. Redémarrez l'API

4. Recréez un compte et reconnectez-vous

## Améliorations apportées

- Meilleure gestion des erreurs avec logs de débogage
- Redirection automatique vers login si token invalide
- Gestion des erreurs 401 dans les intercepteurs axios


