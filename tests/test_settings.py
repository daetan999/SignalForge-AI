from config.settings import Settings


def test_settings_are_read_when_instance_is_created(monkeypatch):
    monkeypatch.setenv("APP_MODE", "vertex")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "event-sandbox")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "asia-southeast1")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-event-model")

    settings = Settings()

    assert settings.app_mode == "vertex"
    assert settings.project_id == "event-sandbox"
    assert settings.location == "asia-southeast1"
    assert settings.model_name == "gemini-event-model"


def test_vertex_mode_rejects_missing_project(monkeypatch):
    monkeypatch.setenv("APP_MODE", "vertex")
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("GCLOUD_PROJECT", raising=False)

    settings = Settings()

    try:
        settings.validate()
    except RuntimeError as exc:
        assert "GOOGLE_CLOUD_PROJECT" in str(exc)
    else:
        raise AssertionError("Vertex mode should require a project ID")
