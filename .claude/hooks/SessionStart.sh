#!/usr/bin/env bash
# Affiché au démarrage d'une session Claude Code

echo ""
echo "=== Projet Maintenance Prédictive ==="

# Vérifier venv
if [ -d ".venv" ]; then
    echo "venv : OK (.venv)"
else
    echo "venv : ABSENT — lancer: python -m venv .venv && pip install -r requirements.txt"
fi

# Vérifier les données
if [ -f "data/raw/PS2.txt" ] && [ -f "data/raw/FS1.txt" ] && [ -f "data/raw/profile.txt" ]; then
    echo "data  : OK (PS2, FS1, profile présents)"
else
    echo "data  : INCOMPLET — vérifier data/raw/"
fi

# Vérifier .env
if [ -f ".env" ]; then
    echo ".env  : OK"
else
    echo ".env  : ABSENT — copier .env.example → .env"
fi

echo ""
