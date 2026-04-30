# Changements

## 2026-04-30 — Correction dashboard Grafana

- Ajout d’un `uid` fixe `prometheus` à la datasource Grafana pour que les panels référencent une source stable.
- Correction du panel `Requêtes totales` pour compter tout le trafic applicatif en excluant `/metrics`.
- Correction des panels `Req/s`, `Requêtes par endpoint` et `Requêtes par statut HTTP` avec `__$rate_interval` et exclusion de `/metrics`.
- Correction des panels de latence `/predict` pour utiliser les buckets cumulés, afin d’éviter les valeurs vides/`NaN` quand le trafic est ponctuel.
- Correction du panel `Taux d'erreur` avec un ratio cumulatif protégé contre la division par zéro.
- Validation effectuée via Prometheus : total, latence médiane `/predict` et taux d’erreur retournent bien des valeurs.
