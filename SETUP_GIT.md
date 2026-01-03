# Setup Git Repository

## Initialiser le dépôt Git

Si ce n'est pas déjà fait, initialisez Git dans ce dossier :

```bash
git init
```

## Ajouter tous les fichiers

```bash
git add .
```

## Faire le premier commit

```bash
git commit -m "Initial commit: Strava Visualization SaaS platform"
```

## Créer un nouveau dépôt sur GitHub

1. Allez sur [GitHub](https://github.com) et créez un nouveau repository
2. **Ne cochez PAS** "Initialize with README" (on a déjà un README)
3. Notez l'URL du repo (ex: `https://github.com/votre-username/strava-visualization-saas.git`)

## Connecter le repo local au repo GitHub

```bash
git remote add origin https://github.com/votre-username/strava-visualization-saas.git
```

## Pousser le code

```bash
git branch -M main
git push -u origin main
```

## Commandes Git utiles

### Voir l'état des fichiers
```bash
git status
```

### Ajouter des changements
```bash
git add .
git commit -m "Description des changements"
git push
```

### Créer une branche pour une nouvelle fonctionnalité
```bash
git checkout -b feature/nom-de-la-feature
# ... faire des changements ...
git add .
git commit -m "Ajout de la fonctionnalité"
git push -u origin feature/nom-de-la-feature
```

## Note importante

⚠️ **N'oubliez pas de configurer vos variables d'environnement** :
- Créez `.env` dans `apps/api/` (copiez depuis `.env.example`)
- Créez `.env.local` dans `apps/web/`
- **Ne commitez JAMAIS** ces fichiers (ils sont dans `.gitignore`)

