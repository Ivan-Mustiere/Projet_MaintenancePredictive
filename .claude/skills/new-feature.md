---
name: new-feature
description: Ajoute une nouvelle feature dans build_features.py avec test associé et vérification de non-régression.
---

Ajoute une nouvelle feature au pipeline de feature engineering en suivant ces étapes :

1. **Implémenter** la feature dans `src/features/build_features.py`
   - Ajouter une fonction `_<nom>_features(arr, prefix)` si c'est une famille de features
   - L'appeler dans `build_features()` et ajouter les colonnes au dict `features`

2. **Tester** dans `tests/test_features.py`
   - Ajouter un test vérifiant que la nouvelle colonne est présente dans le DataFrame
   - Vérifier qu'elle ne produit pas de NaN sur des données aléatoires

3. **Vérifier** la non-régression :
   ```bash
   pytest tests/test_features.py -v
   ```

4. **Documenter** le nom et l'unité de la feature dans le docstring de `build_features()`

5. **Vérifier le leakage** avec `/check-leakage` avant de committer.

Demande à `@feature-engineer` si tu as besoin de conseils sur la pertinence de la feature.
