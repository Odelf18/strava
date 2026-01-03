@echo off
REM Script pour démarrer Celery worker sur Windows

echo Démarrage du worker Celery...
cd /d %~dp0
set PYTHONPATH=%CD%
python -m celery -A app.workers.celery_app worker --loglevel=info --pool=solo

pause

