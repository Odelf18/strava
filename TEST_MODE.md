# Mode Test - Paywall désactivé

## Changements apportés

Le paywall a été temporairement désactivé pour permettre les tests. Vous pouvez maintenant :

1. ✅ Choisir tous les types de packs (Single, All, Premium)
2. ✅ Sélectionner toutes les visualisations
3. ✅ Appliquer tous les filtres
4. ✅ Démarrer le traitement directement sans paiement

## Comment ça fonctionne

Au lieu de rediriger vers Stripe Checkout, le bouton "Start Processing" :
1. Configure le job avec vos choix
2. Démarre immédiatement le traitement
3. Vous redirige vers le dashboard pour suivre la progression

## Workflow de test

1. **Upload** : Uploadez votre fichier ZIP Strava
2. **Configure** : Choisissez vos options sur `/configure/{jobId}`
3. **Start Processing** : Cliquez sur "Start Processing (TEST MODE)"
4. **Dashboard** : Suivez la progression sur le dashboard
5. **Download** : Téléchargez les résultats une fois complété

## Réactiver le paywall

Pour réactiver Stripe plus tard, modifiez `apps/web/app/configure/[jobId]/page.tsx` :

Remplacez :
```typescript
await api.post(`/api/jobs/${jobId}/configure`, {...})
```

Par :
```typescript
const response = await api.post("/api/payment/create-checkout", {...})
window.location.href = response.data.checkout_url
```

Et changez le bouton pour "Proceed to Payment".

## Note

Le code Stripe reste intact et peut être réactivé à tout moment. Seule la page de configuration a été modifiée pour le mode test.


