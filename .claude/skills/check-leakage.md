---
name: check-leakage
description: Vérifie rapidement l'absence de data leakage dans le code modifié. À utiliser avant tout commit sur src/ ou notebooks/.
---

Délègue un audit de data leakage à l'agent spécialisé.

Invoque `@leakage-detector` avec la consigne suivante :

> Audite les fichiers récemment modifiés dans `src/` et `notebooks/` pour détecter tout data leakage.
> Vérifie en priorité :
> - Les appels `fit()` / `fit_transform()` et sur quelles données ils sont appelés
> - L'utilisation de `split_cycles()` vs manipulation manuelle des indices
> - L'accès aux données test (cycles >= 2000) dans les phases 1, 2, 3
>
> Produis un rapport PASS/FAIL avec les lignes exactes si des issues sont trouvées.

Si des leakages sont détectés, les corriger immédiatement avant de continuer.
