# Fix : Erreur Celery sur Windows

## Problème

L'erreur `ValueError: not enough values to unpack (expected 3, got 0)` vient du fait que Celery essaie d'utiliser le pool `prefork` sur Windows, ce qui n'est pas supporté.

## Solution

Forcer l'utilisation du pool `solo` sur Windows dans la configuration Celery.

## Action requise

**Redémarrez le worker Celery** avec le pool `solo` :

```bash
python -m celery -A app.workers.celery_app worker --loglevel=info --pool=solo
```

Ou utilisez le script `start_celery.bat` qui devrait inclure cette option.

## Alternative : Traitement synchrone

Si Celery continue à poser problème, le code est configuré pour fallback sur un traitement synchrone. Vous pouvez aussi traiter directement sans Celery en modifiant temporairement `apps/api/app/routes/jobs.py` pour appeler directement `process_visualization_job(job_id)` au lieu de `.delay()`.

## Note

Le pool `solo` est plus lent que `prefork` mais fonctionne sur Windows. Pour de meilleures performances, utilisez Linux/Mac ou Docker.

