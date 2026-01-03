# Tester l'authentification

## Test rapide avec curl

### 1. Créer un compte

```bash
curl -X POST http://localhost:8000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"test@test.com\", \"password\": \"test123\"}"
```

### 2. Se connecter

```bash
curl -X POST http://localhost:8000/api/auth/login ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=test@test.com&password=test123"
```

Vous devriez recevoir :
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 3. Tester avec le token

Copiez le `access_token` et utilisez-le :

```bash
curl -X GET http://localhost:8000/api/auth/me ^
  -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

## Vérifier dans le navigateur

1. Ouvrez la console (F12)
2. Allez dans l'onglet "Application" > "Local Storage"
3. Vérifiez que `token` existe et contient un JWT

## Problème courant : SECRET_KEY change

Si vous redémarrez l'API sans `.env`, la SECRET_KEY par défaut change et tous les tokens deviennent invalides.

**Solution** : Créez un `.env` avec une SECRET_KEY stable :

```env
SECRET_KEY=my-super-secret-key-that-never-changes
```

Générez une clé sécurisée :
```python
import secrets
print(secrets.token_urlsafe(32))
```


