import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cloud_build_ignore_files_exclude_local_and_secret_state():
    for name in (".dockerignore", ".gcloudignore"):
        patterns = (ROOT / name).read_text(encoding="utf-8")
        assert ".git" in patterns
        assert ".venv" in patterns
        assert ".env" in patterns
        assert "*.zip" in patterns


def test_portable_zip_contains_runtime_but_not_local_environment(tmp_path):
    archive = tmp_path / "signalforge-ai-gcp.zip"
    subprocess.run(
        ["bash", "scripts/package_for_gcp.sh", str(archive)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()

    assert "app.py" in names
    assert "requirements.txt" in names
    assert "sample_data/meridian_discovery_notes.txt" in names
    assert not any(name.startswith((".git/", ".venv/")) for name in names)
    assert ".env" not in names
    assert not any(name.endswith(".zip") for name in names)
