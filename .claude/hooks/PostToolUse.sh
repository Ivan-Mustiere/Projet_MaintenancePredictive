#!/usr/bin/env bash
# Lint automatique après chaque Write/Edit sur un fichier Python

FILE="${CLAUDE_TOOL_RESULT_FILE:-}"

if [[ "$FILE" == *.py ]]; then
    if command -v ruff &>/dev/null; then
        ruff check --fix "$FILE" 2>/dev/null || true
    fi
fi
