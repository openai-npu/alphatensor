#!/bin/bash
# Export winning rank-45 artefacts: JSON and LaTeX

set -e

source "$(dirname "$0")/../.venv/bin/activate"

cd "$(dirname "$0")/../results"

if [ ! -f rank45.json ]; then
  echo "rank45.json not found!"
  exit 1
fi

# Render LaTeX table from rank45.json
python ../evaluation/render_latex.py rank45.json > rank45.tex

echo "Exported rank45.json and rank45.tex"
