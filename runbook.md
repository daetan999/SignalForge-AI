# SignalForge AI — Workshop-Day Runbook

Use this checklist to validate SignalForge AI inside the temporary Google Cloud workshop sandbox. Follow the order exactly: **mock mode first, Vertex AI second, and Cloud Run only if the sandbox permits it**.

## What to bring

Bring these items on your laptop:

- `signalforge-ai-gcp.zip` — this is the only project file you need to upload.
- A backup copy of the ZIP on a USB drive or cloud storage.
- This runbook, available from GitHub or saved offline.

Do **not** upload your `.env`, local `.venv`, credentials, Git history, or real customer documents. The ZIP contains the synthetic Meridian Hospitality demo scenario.

## Part 1 — Create the ZIP before the workshop

Run these commands from your local SignalForge AI repository before leaving for the event:

```bash
git switch main
git pull --ff-only
bash scripts/package_for_gcp.sh
ls -lh signalforge-ai-gcp.zip
```

Confirm that `signalforge-ai-gcp.zip` exists. Save a copy in an easy-to-find location such as Downloads, then make one backup copy.

## Part 2 — Open the correct workshop project

1. Sign in using the temporary workshop or Qwiklabs credentials provided by the organizers.
2. Open the temporary Google Cloud project.
3. Open **Cloud Shell** from the Google Cloud console.
4. Check which project Cloud Shell is using:

```bash
gcloud config get-value project
```

The output should be the temporary workshop project ID. If it prints `(unset)` or shows a personal/company project, stop and ask a facilitator for help before proceeding.

## Part 3 — Upload and extract SignalForge

1. In Cloud Shell, open the three-dot menu.
2. Select **Upload**.
3. Upload `signalforge-ai-gcp.zip`.
4. Run:

```bash
ls -lh ~/signalforge-ai-gcp.zip
mkdir -p ~/signalforge-event
unzip ~/signalforge-ai-gcp.zip -d ~/signalforge-event
cd ~/signalforge-event
test -f app.py && echo "PACKAGE_OK"
```

You should see:

```text
PACKAGE_OK
```

If the ZIP was uploaded under a different filename, use that filename in the `unzip` command.

## Part 4 — Install and test the package

Create an isolated Python environment, install the project, and run its automated tests:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The current package should report:

```text
20 passed
```

If the number is higher in a later version, that is fine. The important result is that all tests pass.

## Part 5 — Prove the app works in mock mode

Always test mock mode before connecting to Vertex AI. This separates application problems from Google Cloud permission or model problems.

```bash
export APP_MODE="mock"
python scripts/validate_environment.py
```

You should see `Environment validation passed.` Then start Streamlit:

```bash
python -m streamlit run app.py \
  --server.port=8080 \
  --server.address=0.0.0.0 \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false
```

In Cloud Shell:

1. Click **Web Preview**.
2. Choose **Preview on port 8080**.
3. In SignalForge, load the bundled demo opportunity.
4. Click **Analyze Opportunity**.

Check that:

- the results dashboard appears;
- the executive overview shows the Meridian Hospitality opportunity;
- confirmed requirements contain evidence and source references;
- discovery gaps and risks appear;
- the recommended next action appears;
- the solution direction and architecture render;
- Markdown, JSON, and DOCX downloads work.

For the current deterministic demo, the headline values should be approximately:

- Discovery coverage: `62%`
- Readiness: `32%`
- Open gaps: `3`
- High risks: `2`

When mock mode works, stop the server with `Ctrl+C` in Cloud Shell.

## Part 6 — Configure Vertex AI

Set the live Google Cloud configuration:

```bash
export GOOGLE_CLOUD_PROJECT="$(gcloud config get-value project)"
export GOOGLE_CLOUD_LOCATION="global"
export GEMINI_MODEL="gemini-2.5-flash"
export GOOGLE_GENAI_USE_VERTEXAI="True"
export APP_MODE="vertex"
```

Confirm the values and active account:

```bash
echo "$GOOGLE_CLOUD_PROJECT"
echo "$GOOGLE_CLOUD_LOCATION"
echo "$GEMINI_MODEL"
gcloud auth list --filter=status:ACTIVE --format="value(account)"
gcloud services list --enabled --filter="NAME:aiplatform.googleapis.com"
```

If the final command does not list `aiplatform.googleapis.com`, ask a facilitator whether you may enable the Vertex AI API. If they approve, run:

```bash
gcloud services enable aiplatform.googleapis.com
```

Do not change IAM roles or permissions yourself unless a facilitator explicitly instructs you to do so.

## Part 7 — Validate one direct Gemini call

First validate the environment:

```bash
python scripts/validate_environment.py
```

Then test one small Gemini request before launching the full app:

```bash
python - <<'PY'
import os
from google import genai

client = genai.Client(
    vertexai=True,
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)

response = client.models.generate_content(
    model=os.environ["GEMINI_MODEL"],
    contents="Reply with the words: VERTEX CONNECTION WORKING",
)

print(response.text)
client.close()
PY
```

If Gemini returns a response, the project, authentication, API, location, and model are working together.

## Part 8 — Run SignalForge with live Vertex AI

Start the same Streamlit app again:

```bash
python -m streamlit run app.py \
  --server.port=8080 \
  --server.address=0.0.0.0 \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false
```

Open **Web Preview → Preview on port 8080**, then verify that the sidebar shows `VERTEX` mode.

Load and analyze the bundled Meridian opportunity again. Live values may differ slightly from mock mode because Gemini performs the extraction. Confirm instead that:

- no customer facts are invented;
- important claims include evidence from the source documents;
- unknown information remains marked as unknown;
- deterministic risks and next-action logic still run;
- all dashboard tabs and downloads work.

This successful Cloud Shell Web Preview is enough for the workshop demo. Cloud Run is optional.

## Part 9 — Optional Cloud Run deployment

Only do this if the facilitator confirms that Cloud Run deployment and unauthenticated access are permitted in the sandbox.

Stop Streamlit with `Ctrl+C`, then run:

```bash
bash scripts/deploy_cloud_run.sh
```

The deployment may ask permission to enable Cloud Run, Cloud Build, or Artifact Registry APIs. Follow the facilitator's instructions. When deployment finishes, retrieve the public URL:

```bash
gcloud run services describe signalforge-ai \
  --region asia-southeast1 \
  --format="value(status.url)"
```

Open the URL and run the Meridian demo once more. If deployment is blocked by permissions, return to Cloud Shell Web Preview; the application itself is still valid.

## Troubleshooting

### `ModuleNotFoundError`

Reactivate the environment and reinstall dependencies:

```bash
cd ~/signalforge-event
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

### Web Preview does not open

Confirm that Streamlit is running on port `8080` with all five Cloud Shell flags shown in this runbook. Then choose **Web Preview → Preview on port 8080** again.

### `403 SERVICE_DISABLED`

The Vertex AI API is not enabled. Ask a facilitator before running:

```bash
gcloud services enable aiplatform.googleapis.com
```

### `403 PERMISSION_DENIED`

Your temporary account does not have the required permission, commonly the Vertex AI User role. Ask a facilitator to fix the workshop account. Do not change IAM yourself.

### Model not found or unavailable

Ask which Gemini model the workshop sandbox supports, then set it without changing the code:

```bash
export GEMINI_MODEL="MODEL_NAME_FROM_FACILITATOR"
```

Restart Streamlit after changing the model.

### Mock mode works but Vertex mode fails

The application is working. The remaining problem is one of the Google Cloud project, API, account permissions, location, model availability, or quota. Show the exact error to a facilitator.

### Cloud Run deployment fails

Use Cloud Shell Web Preview with live Vertex AI. Cloud Run relies on additional build, registry, deployment, and public-access permissions that the temporary sandbox may not provide.

## What to capture after the live run

Take real screenshots only after Vertex mode works:

1. Sidebar showing `VERTEX` mode.
2. Executive overview and headline metrics.
3. Evidence-linked requirements.
4. Discovery gaps.
5. Risk register.
6. Solution direction and architecture.
7. AE-to-SE handoff.
8. Cloud Run URL, if deployment succeeds.

Also download the generated Markdown, JSON, and DOCX outputs. These become the genuine GitHub portfolio assets after the workshop.

## Fast fallback order

If time is running out, use the highest working level:

1. Cloud Run with live Vertex AI.
2. Cloud Shell Web Preview with live Vertex AI.
3. Cloud Shell Web Preview in mock mode.
4. The locally tested mock workflow and saved outputs.

Do not spend the whole workshop fighting Cloud Run. A working live Vertex workflow in Cloud Shell Web Preview proves the important integration.

## Official Google Cloud references

- [Upload files to Cloud Shell](https://docs.cloud.google.com/shell/docs/uploading-and-downloading-files)
- [Use Cloud Shell Web Preview](https://docs.cloud.google.com/shell/docs/using-web-preview)
- [Vertex AI Gemini API quickstart](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart)
- [Deploy source code to Cloud Run](https://docs.cloud.google.com/run/docs/deploying-source-code)
