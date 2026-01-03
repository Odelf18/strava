# Fix : Tâche Celery non enregistrée

## Problème

L'erreur indiquait :
```
Received unregistered task of type 'app.workers.visualization_job.process_visualization_job'.
The message has been ignored and discarded.
```

## Solution

1. **Import automatique dans celery_app.py** : Ajout de `imports=("app.workers.visualization_job",)` dans la configuration Celery
2. **Import explicite** : Import du module `visualization_job` dans `celery_app.py` pour forcer l'enregistrement

## Action requise

**Redémarrez le worker Celery** pour que les changements prennent effet :

1. Arrêtez le worker Celery (Ctrl+C)
2. Redémarrez :
```bash
python -m celery -A app.workers.celery_app worker --loglevel=info
```

Le worker devrait maintenant reconnaître la tâche `process_visualization_job_task`.

## Vérification

Après redémarrage, vous devriez voir dans les logs :
```
[tasks]
  . app.workers.visualization_job.process_visualization_job_task
```

Si la tâche apparaît dans la liste, elle est correctement enregistrée.


