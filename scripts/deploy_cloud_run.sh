#!/usr/bin/env bash
set -euo pipefail

if ! command -v gcloud >/dev/null 2>&1; then
  echo "gcloud CLI is required for Cloud Run deployment." >&2
  exit 1
fi

PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-}"
if [[ -z "$PROJECT_ID" ]]; then
  PROJECT_ID="$(gcloud config get-value project 2>/dev/null)"
fi
if [[ -z "$PROJECT_ID" || "$PROJECT_ID" == "(unset)" ]]; then
  echo "No Google Cloud project detected. Set GOOGLE_CLOUD_PROJECT first." >&2
  exit 1
fi

REGION="${CLOUD_RUN_REGION:-asia-southeast1}"
LOCATION="${GOOGLE_CLOUD_LOCATION:-global}"
MODEL="${GEMINI_MODEL:-gemini-2.5-flash}"

gcloud run deploy signalforge-ai \
  --source . \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars "APP_MODE=vertex,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$LOCATION,GEMINI_MODEL=$MODEL"
