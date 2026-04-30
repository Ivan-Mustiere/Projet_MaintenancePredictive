---
name: eda
description: Lance une analyse exploratoire complète sur les données du projet (PS2, FS1, profile). Produit un résumé avec distributions, shapes et déséquilibre de classes.
---

Effectue une EDA complète sur les données du projet de maintenance prédictive.

## Étapes

1. **Charger les données** via `src/data/load.py` :
   - `load_ps2()` → shape attendue (n_cycles, 6000)
   - `load_fs1()` → shape attendue (n_cycles, 600)
   - `load_profile()` → toutes les colonnes du profile
   - `load_target()` → série binaire

2. **Vérifier la cohérence** :
   - Même nombre de cycles dans les 3 fichiers
   - Aucun NaN
   - Valeurs de `valve_condition` : {100, 90, 80, 73}

3. **Distribution de la cible** :
   - Compter les classes (optimal vs non-optimal)
   - Calculer le ratio de déséquilibre
   - Afficher un barplot

4. **Statistiques descriptives** par classe :
   - Moyenne et std de PS2 et FS1 pour chaque classe
   - Visualiser 3 cycles typiques de chaque classe

5. **Résumé final** :
   - Nombre total de cycles
   - Taille du train (2000) vs test
   - Déséquilibre de classes → recommandation (class_weight, SMOTE, etc.)
   - Anomalies détectées

Utilise `@notebook-analyst` pour générer le notebook `01_exploration.ipynb` si demandé.
