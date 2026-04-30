# Graphe de connaissance du projet

Le codebase `src/` a été analysé via `/graphify` (avril 2026). Les sorties sont dans `graphify-out/`.

| Fichier | Contenu |
|---------|---------|
| `graphify-out/graph.html` | Visualisation interactive — ouvrir dans un navigateur |
| `graphify-out/graph.json` | Données brutes du graphe (GraphRAG-compatible) |
| `graphify-out/GRAPH_REPORT.md` | Rapport d'audit complet |

## Statistiques (avril 2026)
- 45 nœuds · 39 arêtes · 12 communautés — extraits de `src/` par AST

## Communautés
| Communauté | Modules clés |
|------------|-------------|
| Data Loading | `load.py` — load_ps2, load_fs1, load_profile, load_target, load_sensor |
| Model Training Pipelines | `train.py` — baseline, dummy, RF, LightGBM, XGBoost |
| Feature Engineering | `build_features.py` — cycle_stats, fft_features |
| Model Inference | `predict.py` — load_model, predict_cycle |
| Train/Test Split | `split.py` — split_cycles (cycles 0–1999 / 2000–2204) |
| Model Evaluation | `evaluate.py` — compute_metrics, print_report |
| Configuration | `utils/config.py` |

## God nodes (fonctions les plus connectées)
- `build_features()` · `load_sensor()` — 4 arêtes chacune
- `_cycle_stats()` · `_fft_features()` · `train_with_tracking()` — 3 arêtes chacune
- `split_cycles()` — 2 arêtes

## Commandes utiles
- Explorer : `/graphify query "<question>"` ou `/graphify explain "<fonction>"`
- Mettre à jour après modif `src/` : `/graphify src --update`
- Re-visualiser : `/graphify src --cluster-only`
