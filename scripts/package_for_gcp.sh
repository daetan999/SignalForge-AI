#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT="${1:-signalforge-ai-gcp.zip}"
cd "$ROOT_DIR"
zip -r "$OUTPUT" . \
  -x '.git/*' '.venv/*' '__pycache__/*' '.pytest_cache/*' '.env' 'outputs/*' '*.zip'
echo "Created $ROOT_DIR/$OUTPUT"
