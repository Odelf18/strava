# Fix erreur bcrypt avec Python 3.13

## Problème

Erreur : `AttributeError: module 'bcrypt' has no attribute '__about__'`

C'est un problème de compatibilité entre bcrypt et Python 3.13.

## Solution

### Option 1 : Mettre à jour bcrypt (recommandé)

```bash
cd apps/api
pip install --upgrade bcrypt
```

### Option 2 : Utiliser une version spécifique

```bash
pip install bcrypt==4.1.2
```

### Option 3 : Réinstaller passlib et bcrypt

```bash
pip uninstall passlib bcrypt
pip install passlib[bcrypt] bcrypt>=4.0.0
```

## Vérification

Après installation, testez :

```python
python -c "from passlib.context import CryptContext; ctx = CryptContext(schemes=['bcrypt']); print('OK' if ctx.hash('test') else 'KO')"
```

## Si le problème persiste

Utilisez Python 3.11 ou 3.12 au lieu de 3.13 pour éviter les problèmes de compatibilité.


