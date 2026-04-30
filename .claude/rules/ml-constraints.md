# Contraintes ML — Maintenance Prédictive

## Règle absolue : séparation train/test
- Les cycles > 2000 (index >= 2000) sont le **test final sacré**.
- Ne jamais les utiliser pour entraîner, tuner, sélectionner des features, ou fitter un scaler.
- Le split se fait UNIQUEMENT via `src/data/split.py`.

## Anti-leakage
- `StandardScaler`, `MinMaxScaler`, tout `fit()` de preprocessing → uniquement sur `X_train`.
- Appeler `.transform()` sur `X_test`, jamais `.fit_transform()`.

## Reproductibilité
- Toujours passer `random_state=RANDOM_STATE` (depuis `src/utils/config.py`).
- Ne pas hardcoder de seed en dehors de `config.py`.

## Fréquences d'échantillonnage
- PS2 : 100 Hz → 6000 points/cycle
- FS1 : 10 Hz → 600 points/cycle
- Ne jamais concaténer les tableaux bruts PS2 et FS1 directement.
- Agréger par cycle via `src/features/build_features.py` avant tout modèle.
