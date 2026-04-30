# CLAUDE.md — Projet Maintenance Prédictive (ML 2025-2026)

> Fichier de contexte pour Claude Code / assistants IA travaillant sur ce projet.

---

## Contexte

Data Scientist / ML Engineer dans une entreprise industrielle.

Deux objectifs :
1. **Maintenance prédictive** : prédire si la condition de la valve est optimale pour un cycle donné.
2. **Analyse des causes** : expliquer pourquoi la valve est parfois non optimale (SHAP).

---

## Objectif ML

Classification binaire :
- **1 — Optimal** : `valve_condition == 100`
- **0 — Non optimal** : `valve_condition < 100` (valeurs observées : 100, 90, 80, 73)

---

## Données

Source : [UCI – Condition Monitoring of Hydraulic Systems](https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems)

| Fichier                  | Capteur           | Hz  | Points/cycle | Cycles |
|--------------------------|-------------------|-----|--------------|--------|
| `data/raw/PS2.txt`       | Pression (bar)    | 100 | 6 000        | 2 205  |
| `data/raw/FS1.txt`       | Débit (L/min)     | 10  | 600          | 2 205  |
| `data/raw/profile.txt`   | Labels + état sys.| —   | 5 colonnes   | 2 205  |

Colonnes de `profile.txt` (tab-separated, sans header) :
```
cooler_condition | valve_condition | internal_pump_leakage | hydraulic_accumulator | stable_flag
```

**Split : train = cycles 0–1999 (2000 cycles) / test final = cycles 2000–2204 (205 cycles).**

Documentation détaillée dans `docs/documentation.txt`.

---

## Contraintes absolues

1. **Jamais** utiliser les cycles ≥ 2000 pour entraîner, tuner ou sélectionner des features.
2. Tout `fit()` / `fit_transform()` de preprocessing → uniquement sur `X_train`.
3. Le split se fait **exclusivement** via `src/data/split.py` — jamais manuellement.
4. PS2 (100 Hz) et FS1 (10 Hz) ne se concatènent pas bruts — agréger par cycle d'abord.
5. `random_state` toujours depuis `src/utils/config.RANDOM_STATE` (valeur : 42).

---

## État d'avancement

### Infrastructure — FAIT
- [x] Structure complète du projet créée
- [x] Git initialisé (branche `main`)
- [x] `.gitignore` — exclut `.env`, `data/raw/*`, `models/*`, `mlruns/`
- [x] `.env` / `.env.example` — variables d'environnement
- [x] `requirements.txt` + `pyproject.toml` (ruff, black, pytest)
- [x] `Dockerfile` + `docker-compose.yml` (API + MLflow + Prometheus + Grafana)
- [x] `run.sh` — script de gestion (up/stop/rebuild/logs/install/test/train…)
- [x] `.github/workflows/ci.yml` — lint + tests + docker build
- [x] `dvc.yaml` — pipeline features → train
- [x] `.claude/` — agents, skills, commands, rules, hooks

### Code source — FAIT
- [x] `src/utils/config.py` — centralise chemins et paramètres
- [x] `src/data/load.py` — chargement PS2, FS1, profile, target
- [x] `src/data/split.py` — split train/test strict
- [x] `src/features/build_features.py` — stats temporelles + FFT par cycle
- [x] `src/models/train.py` — pipelines baseline + RF avec MLflow
- [x] `src/models/predict.py` — chargement modèle + inférence
- [x] `src/models/evaluate.py` — métriques + rapport
- [x] `app/main.py` — API FastAPI `/predict` + `/health` + métriques Prometheus
- [x] `tests/` — test_data, test_features, test_model

### ML — FAIT
- [x] Blocs `__main__` dans `build_features.py` et `train.py`
- [x] venv créé + dépendances installées
- [x] `data/processed/features.parquet` — 2205 cycles × 41 features
- [x] Modèles entraînés : Dummy, LogReg, RF, XGBoost, LightGBM + Optuna (RF)
- [x] `models/model.joblib` — meilleur modèle déployé (RF tuné)
- [x] 11/11 tests unitaires passent
- [x] Notebooks 01 à 04 créés

### Résultats CV (train — 5-fold stratifié)
| Modèle             | F1     | ROC-AUC | Accuracy |
|--------------------|--------|---------|----------|
| LogReg (baseline)  | 0.9991 | 0.9995  | 0.9990   |
| Random Forest      | 0.9986 | 1.0000  | 0.9985   |
| RF tuné (Optuna)   | 0.9981 | 1.0000  | 0.9980   |
| LightGBM           | 0.9967 | 0.9999  | 0.9965   |
| XGBoost            | 0.9957 | 1.0000  | 0.9955   |
| Dummy              | 0.6894 | 0.5000  | 0.5260   |

**Modèle déployé** : `models/model.joblib` (RF tuné — params Optuna : n_estimators=382, max_depth=9)

### À FAIRE
- [ ] `./run.sh up` — démarrer la stack Docker
- [ ] Exécuter les notebooks (EDA + évaluation finale sur test set)
- [ ] SHAP sur le test set (notebook 04)

### Livraison — À FAIRE
- [ ] Dépôt GitHub public
- [ ] Notebooks finalisés (01 à 04)
- [ ] Dashboard Grafana configuré
- [ ] DVC remote configuré
- [ ] README.md complété

---

## Architecture

```
├── data/
│   ├── raw/               # PS2.txt, FS1.txt, profile.txt (ignorés git, versionnés DVC)
│   └── processed/         # features.parquet (généré par run.sh features)
├── docs/                  # documentation.txt, description.txt
├── src/
│   ├── data/              # load.py, split.py
│   ├── features/          # build_features.py
│   ├── models/            # train.py, predict.py, evaluate.py
│   └── utils/             # config.py
├── app/                   # FastAPI — POST /predict, GET /health, GET /metrics
├── tests/                 # pytest
├── notebooks/             # 01_exploration … 04_evaluation
├── models/                # model.joblib (ignoré git, versionné MLflow/DVC)
├── monitoring/            # prometheus.yml + grafana/provisioning/
├── .github/workflows/     # ci.yml
├── .claude/               # agents, skills, commands, rules, hooks
├── docker-compose.yml
├── Dockerfile
├── run.sh                 # point d'entrée principal
├── dvc.yaml
├── requirements.txt
├── pyproject.toml
└── .env                   # non commité
```

---

## Commandes principales

```bash
./run.sh help              # liste toutes les commandes disponibles
./run.sh install           # créer .venv + pip install -r requirements.txt
./run.sh features          # construire data/processed/features.parquet
./run.sh train             # entraîner le modèle (log dans MLflow)
./run.sh test              # pytest avec couverture
./run.sh lint              # ruff + black
./run.sh up                # démarrer toute la stack Docker
./run.sh logs api          # logs live du service API
./run.sh rebuild api       # reconstruire l'image Docker du service api
./run.sh shell api         # shell interactif dans le conteneur
./run.sh mlflow            # ouvrir l'UI MLflow dans le navigateur
```

Accès services (stack Docker) :
- API docs   : http://localhost:8000/docs
- MLflow     : http://localhost:5000
- Prometheus : http://localhost:9090
- Grafana    : http://localhost:3000 (admin/admin)

---

## Agents disponibles (`@nom`)

| Agent               | Quand l'utiliser |
|---------------------|-----------------|
| `@data-validator`   | Avant le feature engineering — valide shapes, NaN, distribution cible |
| `@feature-engineer` | Ajouter / modifier des features dans `build_features.py` |
| `@ml-trainer`       | Entraîner, comparer, optimiser les modèles |
| `@leakage-detector` | Avant chaque commit — auditer pour data leakage |
| `@notebook-analyst` | Rédiger ou enrichir les notebooks Jupyter |

## Skills disponibles (`/nom`)

| Skill             | Action |
|-------------------|--------|
| `/eda`            | Analyse exploratoire complète |
| `/check-leakage`  | Vérification anti-leakage rapide |
| `/new-feature`    | Ajouter une feature avec test associé |
| `/evaluate-model` | Évaluation finale sur le test set + SHAP |
| `/test`           | Lancer pytest avec couverture |
| `/train`          | Entraîner le modèle |
| `/lint`           | ruff + black |
| `/stack`          | Aide docker compose |

---

## Stack technique

| Domaine          | Outil                              |
|------------------|------------------------------------|
| ML               | scikit-learn, XGBoost, LightGBM    |
| Données          | pandas, numpy, scipy               |
| Feature eng.     | scipy FFT, tsfresh (optionnel)     |
| Tracking         | MLflow                             |
| Versioning data  | DVC                                |
| API              | FastAPI + uvicorn                  |
| Monitoring       | Prometheus + Grafana               |
| Tests            | pytest + pytest-cov                |
| Lint / Format    | ruff + black                       |
| Docker           | docker compose                     |
| CI/CD            | GitHub Actions                     |

---

## Points d'attention

- **Déséquilibre de classes** : vérifier la distribution de `valve_condition` — utiliser F1 comme métrique principale si déséquilibre.
- **Leakage** : utiliser `/check-leakage` avant tout commit sur `src/` ou les notebooks.
- `data/raw/` et `models/` exclus du git (`data/raw/*` dans `.gitignore`) — gérer via DVC.
- **Reproductibilité** : `RANDOM_STATE=42` dans `.env`, à passer à tous les estimateurs.

---

*Dernière mise à jour : avril 2026*
