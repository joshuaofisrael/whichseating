#!/bin/bash
# Build, QA, legal gate. Usage: ./deploy.sh [--launch]
# Does not commit. Commit and push main yourself after this passes.
# --launch keeps INDEXABLE false in config and overrides it for this run.
# Set GA4_ID in _build/config.py first. An empty ID fails check.py.
set -e
cd "$(dirname "$0")"
MODE=""
[ "$1" = "--launch" ] && MODE="--launch"
python3 _build/build.py $MODE
python3 _build/check.py $MODE
python3 _build/legal_gate.py check
echo "Build passed ($MODE). Commit the generated site and push main for GitHub Pages."
