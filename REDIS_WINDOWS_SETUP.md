# Configuration Redis sur Windows

## Problème

Redis ne démarre pas avec l'erreur :
```
bind: No such file or directory
```

## Solutions

### Option 1: Utiliser Redis via WSL (Recommandé)

Si vous avez WSL (Windows Subsystem for Linux) installé :

```bash
# Dans WSL
sudo apt-get update
sudo apt-get install redis-server
redis-server
```

Puis dans votre `.env` de l'API, utilisez :
```
REDIS_URL=redis://localhost:6379/0
```

### Option 2: Utiliser Memurai (Redis pour Windows)

Memurai est une alternative native Windows à Redis :

1. Téléchargez depuis : https://www.memurai.com/get-memurai
2. Installez Memurai
3. Il démarre automatiquement comme service Windows
4. Utilisez la même configuration que Redis

### Option 3: Utiliser Docker

Si vous avez Docker Desktop :

```bash
docker run -d -p 6379:6379 redis:latest
```

### Option 4: Utiliser Upstash (Cloud Redis - Gratuit)

Pour le développement, vous pouvez utiliser Upstash (gratuit jusqu'à 10K commandes/jour) :

1. Créez un compte sur https://upstash.com
2. Créez une base Redis
3. Copiez l'URL de connexion
4. Utilisez-la dans votre `.env` :
```
REDIS_URL=redis://default:password@host:port
```

### Option 5: Désactiver temporairement Celery (Développement uniquement)

Pour tester l'API sans Redis, vous pouvez modifier temporairement le code pour exécuter les tâches de manière synchrone. **Attention : ce n'est pas recommandé pour la production.**

## Configuration recommandée pour le développement

Utilisez **Docker** ou **Upstash** pour le développement local, c'est le plus simple.

## Vérification

Une fois Redis/Memurai/Upstash configuré, testez la connexion :

```python
import redis
r = redis.from_url("redis://localhost:6379/0")
r.ping()  # Devrait retourner True
```


