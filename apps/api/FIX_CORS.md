# Fix CORS et erreur 500

## Problème 1 : CORS

Si vous avez une erreur CORS, vérifiez :

1. **L'API est-elle démarrée ?**
```bash
cd apps/api
python run.py
```

2. **Le fichier .env existe-t-il ?**
```bash
cd apps/api
# Si .env n'existe pas, créez-le :
# CORS_ORIGINS=["http://localhost:3000"]
```

3. **Redémarrez l'API** après modification de .env

## Problème 2 : Erreur 500

L'erreur 500 peut venir de :

1. **Base de données non initialisée**
   - L'API crée automatiquement les tables au premier démarrage
   - Vérifiez les logs de l'API pour voir l'erreur exacte

2. **Vérifiez les logs dans le terminal où l'API tourne**

## Solution rapide

1. **Créez/éditez `.env` dans `apps/api/` :**
```env
DEBUG=True
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

2. **Redémarrez l'API**

3. **Vérifiez que la base de données est créée :**
   - Un fichier `strava_saas.db` devrait apparaître dans `apps/api/`

## Test rapide

Testez l'API directement :
```bash
curl http://localhost:8000/api/health
```

Devrait retourner : `{"status":"ok"}`


