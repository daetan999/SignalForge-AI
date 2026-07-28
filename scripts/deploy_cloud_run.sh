#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project)}"
REGION="${CLOUD_RUN_REGION:-asia-southeast1}"
LOCATION="${GOOGLE_CLOUD_LOCATION:-global}"
MODEL="${GEMINI_MODEL:-gemini-2.5-flash}"

gcloud run deploy signalforge-ai \
  --source . \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars "APP_MODE=vertex,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$LOCATION,GEMINI_MODEL=$MODEL"
