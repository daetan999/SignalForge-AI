#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT="${1:-signalforge-ai-gcp.zip}"
cd "$ROOT_DIR"
zip -r "$OUTPUT" . \
  -x '.git/*' '.venv/*' '__pycache__/*' '*/__pycache__/*' '.pytest_cache/*' \
    '.ruff_cache/*' '.env' 'outputs/*' '*.zip' '.coverage' 'htmlcov/*' \
    '.DS_Store' '*/.DS_Store'
echo "Created $OUTPUT"
