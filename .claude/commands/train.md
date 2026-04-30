---
description: Entraîner le modèle et logguer dans MLflow
---

Lance le pipeline d'entraînement complet :
1. Construction des features (PS2 + FS1)
2. Split train/test (2000 premiers cycles)
3. Entraînement avec cross-validation
4. Logging MLflow

```bash
python -m src.models.train
```

Pour voir les résultats : http://localhost:5000
