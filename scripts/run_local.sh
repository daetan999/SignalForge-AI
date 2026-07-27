#!/usr/bin/env bash
set -euo pipefail
export APP_MODE="${APP_MODE:-mock}"
streamlit run app.py --server.port "${PORT:-8080}" --server.address 0.0.0.0
