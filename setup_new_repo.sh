#!/bin/bash

# Script pour migrer vers un nouveau dépôt GitHub personnel

echo "🚀 Configuration d'un nouveau dépôt GitHub personnel"
echo ""

# Demander l'URL du nouveau repo
read -p "Entrez l'URL de votre nouveau repo GitHub (ex: https://github.com/votre-username/strava-visualization-saas.git): " NEW_REPO_URL

if [ -z "$NEW_REPO_URL" ]; then
    echo "❌ URL vide, annulation."
    exit 1
fi

echo ""
echo "📦 Ajout de tous les fichiers..."
git add .

echo ""
echo "💾 Création du commit..."
git commit -m "Initial commit: Strava Visualization SaaS platform with FastAPI and Next.js" || echo "⚠️  Pas de nouveaux changements à commiter"

echo ""
echo "🔄 Changement du remote..."
git remote remove origin 2>/dev/null || echo "⚠️  Remote origin n'existe pas ou déjà supprimé"
git remote add origin "$NEW_REPO_URL"

echo ""
echo "📤 Poussée vers le nouveau repo..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Terminé! Votre code est maintenant sur: $NEW_REPO_URL"
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Configurez vos variables d'environnement (.env dans apps/api et .env.local dans apps/web)"
echo "   2. Suivez le guide DEPLOYMENT.md pour déployer"
echo "   3. Configurez Stripe avec vos clés API"

