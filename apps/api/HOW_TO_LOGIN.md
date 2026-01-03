# Comment se connecter

## 1. Démarrer les services

### Terminal 1 - API FastAPI
```bash
cd apps/api
python run.py
```
L'API sera accessible sur http://localhost:8000

### Terminal 2 - Frontend Next.js
```bash
cd apps/web
npm run dev
```
Le frontend sera accessible sur http://localhost:3000

## 2. Créer un compte

1. Ouvrez votre navigateur : http://localhost:3000
2. Cliquez sur "Sign Up" ou allez sur http://localhost:3000/auth/register
3. Entrez votre email et mot de passe
4. Cliquez sur "Sign Up"

## 3. Se connecter

1. Allez sur http://localhost:3000/auth/login
2. Entrez votre email et mot de passe
3. Cliquez sur "Login"

Vous serez redirigé vers le dashboard : http://localhost:3000/dashboard

## 4. Utiliser l'API directement (optionnel)

### Créer un compte via API
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Se connecter via API
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

Vous recevrez un token JWT dans la réponse :
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Utiliser le token pour les requêtes authentifiées
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

## 5. Tester avec l'interface Swagger

1. Allez sur http://localhost:8000/docs
2. Cliquez sur "POST /api/auth/register"
3. Cliquez sur "Try it out"
4. Entrez vos données :
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```
5. Cliquez sur "Execute"
6. Ensuite, utilisez "POST /api/auth/login" pour vous connecter
7. Cliquez sur le cadenas en haut à droite et entrez le token reçu

## Problèmes courants

### "Could not validate credentials"
- Vérifiez que vous utilisez le bon token
- Le token expire après 24h par défaut
- Reconnectez-vous pour obtenir un nouveau token

### "Email already registered"
- L'email est déjà utilisé
- Utilisez un autre email ou connectez-vous directement

### CORS errors
- Vérifiez que `CORS_ORIGINS` dans `.env` inclut `http://localhost:3000`
- Redémarrez l'API après modification


