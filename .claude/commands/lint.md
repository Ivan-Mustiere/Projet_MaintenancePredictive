---
description: Vérifier et corriger le style du code (ruff + black)
---

Vérifie le code avec ruff et black.

```bash
ruff check src/ app/ tests/ --fix && black src/ app/ tests/
```
