@echo off
REM Script Windows pour migrer vers un nouveau dépôt GitHub personnel

echo 🚀 Configuration d'un nouveau dépôt GitHub personnel
echo.

REM Demander l'URL du nouveau repo
set /p NEW_REPO_URL="Entrez l'URL de votre nouveau repo GitHub (ex: https://github.com/votre-username/strava-visualization-saas.git): "

if "%NEW_REPO_URL%"=="" (
    echo ❌ URL vide, annulation.
    exit /b 1
)

echo.
echo 📦 Ajout de tous les fichiers...
git add .

echo.
echo 💾 Création du commit...
git commit -m "Initial commit: Strava Visualization SaaS platform with FastAPI and Next.js" || echo ⚠️  Pas de nouveaux changements à commiter

echo.
echo 🔄 Changement du remote...
git remote remove origin 2>nul || echo ⚠️  Remote origin n'existe pas ou déjà supprimé
git remote add origin "%NEW_REPO_URL%"

echo.
echo 📤 Poussée vers le nouveau repo...
git branch -M main
git push -u origin main

echo.
echo ✅ Terminé! Votre code est maintenant sur: %NEW_REPO_URL%
echo.
echo 📝 Prochaines étapes:
echo    1. Configurez vos variables d'environnement (.env dans apps/api et .env.local dans apps/web)
echo    2. Suivez le guide DEPLOYMENT.md pour déployer
echo    3. Configurez Stripe avec vos clés API

pause

