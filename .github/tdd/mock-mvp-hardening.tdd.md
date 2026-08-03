# Mock MVP hardening — TDD evidence

## Source and user journeys

The journeys were derived from the agreed SignalForge MVP plan:

1. A seller can analyze the synthetic opportunity locally and receive a complete workspace without GCP access.
2. An uploaded customer document never inherits fictional Meridian or Google Cloud facts that are absent from the source.
3. Qualification tools expose unresolved security, scale, commercial, and delivery risks and choose the next action deterministically.
4. The same application can switch to Vertex AI through runtime configuration without changing source code.
5. The event package can be uploaded to Cloud Shell without local environments, credentials, caches, or Git state.

## RED and GREEN checkpoints

| Behavior | RED evidence | GREEN evidence |
|---|---|---|
| Grounded mock extraction and Streamlit demo | `b94a78a` — 3 failures in the new target suite | `873da76` — full suite passed after the grounded extractor and UI key were implemented |
| Runtime settings, injectable Vertex boundary, retry, packaging ignores, unknown-scale risk | `9e65335` — 6 intended failures | `00d35ff` — target suite 7 passed; full suite 18 passed |
| Confirmed scale is distinguished from an explicit unknown | `13b74c5` — focused test failed | `04822e0` — focused and full suites passed |

## Test guarantees

| # | What is guaranteed | Test target | Type |
|---|---|---|---|
| 1 | Arbitrary uploads do not receive Meridian, hospitality, or Google Cloud defaults | `tests/test_mock_provider.py` | Unit |
| 2 | Every confirmed mock requirement includes source evidence | `tests/test_mock_provider.py` | Unit |
| 3 | Complete low-risk opportunities proceed, while high risk blocks progression | `tests/test_decisions.py` | Unit |
| 4 | Explicitly unknown scale remains a technical risk even when latency is known | `tests/test_mvp.py` | Unit |
| 5 | Runtime settings are resolved when a `Settings` instance is created | `tests/test_settings.py` | Unit |
| 6 | The Vertex provider uses the configured model, validates structured output, retries once, and closes its client | `tests/test_provider_boundary.py` | Integration boundary |
| 7 | The ZIP includes required runtime files and excludes local or secret state | `tests/test_packaging.py` | Integration |
| 8 | The Streamlit demo loads, analyzes Meridian, and renders the expected metrics | `tests/test_streamlit_app.py` | Application/E2E |

## Coverage and known gaps

The final evidence commands and exact results are recorded in draft PR #2. Live Vertex AI, Application Default Credentials, and Cloud Run deployment cannot be exercised without the temporary workshop GCP project; they remain explicit event-day validation steps.
