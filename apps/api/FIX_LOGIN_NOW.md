# Fix immédiat : Problème de login

## Problème

Erreur : `JWT decode error: Subject must be a string.`

Le JWT est créé avec `user.id` (entier) mais `jose` JWT exige que le sujet soit une string.

## Solution appliquée

Le code a été corrigé pour convertir `user.id` en string lors de la création du token.

## Action requise

**Redémarrez l'API** pour que les changements prennent effet :

1. Arrêtez l'API (Ctrl+C)
2. Redémarrez :
```bash
python run.py
```

3. **Reconnectez-vous** :
   - Allez sur http://localhost:3000/auth/login
   - Entrez votre email et mot de passe
   - Le login devrait maintenant fonctionner

## Si vous avez encore un token invalide

1. Ouvrez la console du navigateur (F12)
2. Tapez :
```javascript
localStorage.removeItem("token")
```
3. Reconnectez-vous

Le nouveau token sera créé correctement avec le code corrigé.


