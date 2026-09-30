#!/usr/bin/env bash
# filepath: ./frontend/build_ui.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UI_DIR="$ROOT_DIR/frontend"

source "$ROOT_DIR/.venv/bin/activate"

for ui_file in "$UI_DIR"/*.ui; do
    [ -e "$ui_file" ] || continue

    py_file="${ui_file%.ui}.py"
    echo "Building $(basename "$ui_file")..."
    pyside6-uic "$ui_file" -o "$py_file"
done

echo "UI build completed."