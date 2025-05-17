#!/bin/bash
# One-command launcher for RL training

set -e

# Activate virtual environment (project root .venv)
source "$(dirname "$0")/../../.venv/bin/activate"
# Install dependencies
uv pip install -r "$(dirname "$0")/../requirements.txt"

# source "$(dirname "$0")/../.venv/bin/activate"
# pip install -r "$(dirname "$0")/../requirements.txt"

# Ensure project package path is available to Ray workers
export PYTHONPATH="$PYTHONPATH:$(cd "$(dirname "$0")/.." && pwd)"

python "$(dirname "$0")/../training/train.py" "$@"
