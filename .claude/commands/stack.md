---
description: Démarrer / arrêter la stack Docker complète
---

**Démarrer :**
```bash
docker compose up -d
```

**Vérifier :**
```bash
docker compose ps
```

**Arrêter :**
```bash
docker compose down
```

**Accès :**
- API FastAPI : http://localhost:8000/docs
- MLflow UI  : http://localhost:5000
- Prometheus : http://localhost:9090
- Grafana    : http://localhost:3000 (admin/admin)
