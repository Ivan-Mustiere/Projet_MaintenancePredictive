#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# run.sh — Gestion du projet Maintenance Prédictive
# ============================================================
# Usage : ./run.sh <commande> [options]
#
# Commandes disponibles :
#   up          Démarrer la stack Docker
#   stop        Arrêter la stack (conteneurs conservés)
#   down        Arrêter et supprimer les conteneurs
#   restart     Redémarrer la stack
#   rebuild     Reconstruire les images et redémarrer
#   logs        Afficher les logs (tous ou un service)
#   status      État des conteneurs
#   shell       Ouvrir un shell dans un conteneur
#   install     Créer le venv et installer les dépendances
#   test        Lancer les tests unitaires
#   lint        Vérifier le style du code (ruff + black)
#   train       Lancer l'entraînement du modèle
#   features    Construire les features depuis les données brutes
#   mlflow      Ouvrir l'UI MLflow dans le navigateur
#   help        Afficher cette aide
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }

# Charger .env si présent
[ -f .env ] && export $(grep -v '^#' .env | xargs) 2>/dev/null || true

CMD="${1:-help}"

case "$CMD" in

  # ----------------------------------------------------------
  up)
    info "Démarrage de la stack..."
    docker compose up -d
    success "Stack démarrée."
    echo ""
    echo "  API FastAPI : http://localhost:${APP_PORT:-8000}/docs"
    echo "  MLflow UI   : http://localhost:5000"
    echo "  Prometheus  : http://localhost:${PROMETHEUS_PORT:-9090}"
    echo "  Grafana     : http://localhost:${GRAFANA_PORT:-3000}  (admin/admin)"
    ;;

  # ----------------------------------------------------------
  stop)
    info "Arrêt des conteneurs (données conservées)..."
    docker compose stop
    success "Conteneurs arrêtés."
    ;;

  # ----------------------------------------------------------
  down)
    info "Suppression des conteneurs..."
    docker compose down
    success "Conteneurs supprimés."
    ;;

  # ----------------------------------------------------------
  restart)
    info "Redémarrage de la stack..."
    docker compose restart
    success "Stack redémarrée."
    ;;

  # ----------------------------------------------------------
  rebuild)
    SERVICE="${2:-}"
    info "Reconstruction des images${SERVICE:+ ($SERVICE)}..."
    if [ -n "$SERVICE" ]; then
      docker compose build "$SERVICE"
      docker compose up -d "$SERVICE"
    else
      docker compose build
      docker compose up -d
    fi
    success "Rebuild terminé."
    ;;

  # ----------------------------------------------------------
  logs)
    SERVICE="${2:-}"
    LINES="${3:-100}"
    if [ -n "$SERVICE" ]; then
      docker compose logs -f --tail="$LINES" "$SERVICE"
    else
      docker compose logs -f --tail="$LINES"
    fi
    ;;

  # ----------------------------------------------------------
  status)
    docker compose ps
    ;;

  # ----------------------------------------------------------
  shell)
    SERVICE="${2:-api}"
    info "Ouverture d'un shell dans '$SERVICE'..."
    docker compose exec "$SERVICE" /bin/bash || \
    docker compose exec "$SERVICE" /bin/sh
    ;;

  # ----------------------------------------------------------
  install)
    info "Création du venv et installation des dépendances..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    success "Installation terminée. Activer avec : source .venv/bin/activate"
    ;;

  # ----------------------------------------------------------
  test)
    info "Lancement des tests..."
    ARGS="${*:2}"
    source .venv/bin/activate 2>/dev/null || true
    pytest ${ARGS:---cov=src --cov-report=term-missing -v}
    ;;

  # ----------------------------------------------------------
  lint)
    info "Vérification du style (ruff + black)..."
    source .venv/bin/activate 2>/dev/null || true
    ruff check src/ app/ tests/ --fix
    black src/ app/ tests/
    success "Lint terminé."
    ;;

  # ----------------------------------------------------------
  features)
    info "Construction des features depuis data/raw/..."
    source .venv/bin/activate 2>/dev/null || true
    python -m src.features.build_features
    success "Features construites dans data/processed/"
    ;;

  # ----------------------------------------------------------
  train)
    info "Lancement de l'entraînement..."
    source .venv/bin/activate 2>/dev/null || true
    python -m src.models.train
    success "Entraînement terminé. Résultats : http://localhost:5000"
    ;;

  # ----------------------------------------------------------
  notebooks)
    info "Exécution des notebooks 01 → 04..."
    source .venv/bin/activate 2>/dev/null || true
    for nb in notebooks/01_exploration.ipynb \
              notebooks/02_feature_engineering.ipynb \
              notebooks/03_modeling.ipynb \
              notebooks/04_evaluation.ipynb; do
      info "  → $nb"
      python - "$nb" <<'PYEOF'
import sys, uuid, nbformat
path = sys.argv[1]
nb = nbformat.read(path, as_version=4)
for cell in nb.cells:
    if not cell.get("id"):
        cell["id"] = uuid.uuid4().hex[:8]
nbformat.write(nb, path)
PYEOF
      jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=600 \
        --ExecutePreprocessor.kernel_name=python3 \
        "$nb"
      success "  $nb terminé"
    done
    success "Tous les notebooks exécutés."
    ;;

  # ----------------------------------------------------------
  mlflow)
    URL="http://localhost:5000"
    info "Ouverture de MLflow : $URL"
    if command -v xdg-open &>/dev/null; then
      xdg-open "$URL"
    elif command -v open &>/dev/null; then
      open "$URL"
    else
      warn "Ouvrir manuellement : $URL"
    fi
    ;;

  # ----------------------------------------------------------
  help|--help|-h)
    echo ""
    echo "Usage : ./run.sh <commande> [options]"
    echo ""
    echo "  Stack Docker"
    echo "    up                      Démarrer tous les services"
    echo "    stop                    Arrêter les conteneurs (données conservées)"
    echo "    down                    Supprimer les conteneurs"
    echo "    restart                 Redémarrer tous les services"
    echo "    rebuild [service]       Reconstruire l'image (tous ou un seul)"
    echo "    logs [service] [lignes] Afficher les logs en live"
    echo "    status                  État des conteneurs"
    echo "    shell [service]         Shell interactif (défaut: api)"
    echo ""
    echo "  Développement local"
    echo "    install                 Créer .venv et installer requirements.txt"
    echo "    test [args]             Lancer pytest (args optionnels)"
    echo "    lint                    ruff + black sur src/ app/ tests/"
    echo "    features                Construire les features ML"
    echo "    train                   Entraîner le modèle"
    echo "    notebooks               Exécuter les notebooks 01 à 04"
    echo "    mlflow                  Ouvrir l'UI MLflow"
    echo ""
    ;;

  *)
    error "Commande inconnue : '$CMD'. Lancer './run.sh help' pour la liste."
    ;;

esac
