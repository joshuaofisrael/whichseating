#!/bin/bash
# Build, QA, legal gate. Usage: ./deploy.sh [--launch]
# Does not commit. Commit and push main yourself after this passes.
set -e
cd "$(dirname "$0")"
MODE=""
[ "$1" = "--launch" ] && MODE="--launch"
python3 _build/build.py $MODE
python3 _build/check.py $MODE
python3 _build/legal_gate.py check
echo "Build passed ($MODE). Commit the generated site and push main for GitHub Pages."
