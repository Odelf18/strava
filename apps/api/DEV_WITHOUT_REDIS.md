# Développement sans Redis (Mode synchrone)

⚠️ **ATTENTION**: Ce mode est uniquement pour le développement et les tests. Ne l'utilisez pas en production.

## Pourquoi ?

Par défaut, Celery nécessite Redis pour la queue de tâches. Si vous ne pouvez pas installer Redis sur Windows, vous pouvez temporairement exécuter les tâches de manière synchrone.

## Modification temporaire

Dans `apps/api/app/routes/payment.py`, modifiez la ligne qui déclenche la tâche Celery :

**Avant (asynchrone avec Celery) :**
```python
from app.workers.visualization_job import process_visualization_job
process_visualization_job.delay(job_id)
```

**Après (synchrone, sans Celery) :**
```python
from app.workers.visualization_job import process_visualization_job
process_visualization_job(job_id)  # Appel direct, pas .delay()
```

## Limitations

- Les requêtes HTTP seront bloquantes pendant le traitement
- Pas de suivi de progression en temps réel
- Pas de gestion des timeouts
- Performance réduite

## Recommandation

Utilisez plutôt :
1. **Docker** : `docker run -d -p 6379:6379 redis`
2. **Upstash** (gratuit) : https://upstash.com
3. **WSL** si disponible

Ces solutions sont meilleures pour le développement.


