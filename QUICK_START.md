# 🚀 Quick Start - Créer votre repo personnel

## Étapes rapides

### 1. Créer le repo sur GitHub

1. Allez sur https://github.com/new
2. Nommez votre repo (ex: `strava-visualization-saas`)
3. **Ne cochez PAS** "Initialize with README"
4. Cliquez sur "Create repository"
5. **Copiez l'URL** du repo (ex: `https://github.com/votre-username/strava-visualization-saas.git`)

### 2. Exécuter le script de migration

**Sur Windows:**
```bash
setup_new_repo.bat
```

**Sur Mac/Linux:**
```bash
chmod +x setup_new_repo.sh
./setup_new_repo.sh
```

Le script va:
- ✅ Ajouter tous les fichiers
- ✅ Créer un commit
- ✅ Changer le remote vers votre nouveau repo
- ✅ Pousser le code

### 3. Alternative manuelle

Si vous préférez faire ça manuellement:

```bash
# 1. Ajouter tous les fichiers
git add .

# 2. Créer un commit
git commit -m "Initial commit: Strava Visualization SaaS platform"

# 3. Changer le remote (remplacez par votre URL)
git remote remove origin
git remote add origin https://github.com/votre-username/strava-visualization-saas.git

# 4. Pousser vers votre repo
git push -u origin main
```

## ✅ C'est fait!

Votre code est maintenant sur votre repo personnel. Vous pouvez:
- 🔒 Le garder privé (recommandé pour un SaaS)
- 🌐 Le rendre public si vous voulez
- 🚀 Commencer à déployer (voir DEPLOYMENT.md)

## ⚠️ Important

N'oubliez pas de:
1. Configurer `.env` dans `apps/api/` (copiez depuis `.env.example`)
2. Configurer `.env.local` dans `apps/web/`
3. **Ne jamais commiter** ces fichiers (ils sont dans `.gitignore`)

