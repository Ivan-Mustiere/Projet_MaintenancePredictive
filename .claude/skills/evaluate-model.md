---
name: evaluate-model
description: Évalue le modèle sauvegardé sur le test final (cycles > 2000) et produit le rapport complet de métriques.
---

Évalue le modèle entraîné sur le test final. Ce skill ne doit être utilisé qu'une fois le modèle final sélectionné.

## Avertissement
Le test final (cycles >= 2000) est sacré. Cette évaluation est **définitive** — ne pas l'utiliser pour ajuster le modèle.

## Étapes

1. **Charger le modèle** depuis `models/model.joblib`
2. **Charger les features** depuis `data/processed/features.parquet`
3. **Récupérer le test set** via `split_cycles()` — uniquement `X_test` et `y_test`
4. **Prédire** avec `predict_cycle()` de `src/models/predict.py`
5. **Calculer les métriques** via `src/models/evaluate.py` :
   - Accuracy, Precision, Recall, F1
   - ROC-AUC
   - Matrice de confusion
   - Classification report complet
6. **Logger dans MLflow** avec le tag `evaluation=final_test`
7. **Produire le notebook 04** via `@notebook-analyst` avec SHAP

## Sortie attendue
```
=== Évaluation finale (test set) ===
Cycles testés : N
Accuracy  : X.XXX
F1-score  : X.XXX
ROC-AUC   : X.XXX

Matrice de confusion :
[[TN  FP]
 [FN  TP]]
```
