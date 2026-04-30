# Style de code

- Longueur de ligne max : 100 caractères (ruff + black configurés dans pyproject.toml).
- Type hints obligatoires sur toutes les fonctions publiques.
- Pas de commentaires qui décrivent ce que le code fait — seulement le pourquoi si non évident.
- Imports : stdlib → third-party → src (séparés par une ligne vide).
- Pas de `print()` dans `src/` — utiliser `logging` si nécessaire.
