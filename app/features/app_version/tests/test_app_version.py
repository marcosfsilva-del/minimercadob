from app.features.app_version.service import status


def test_status():
    assert status() == {"feature": "app-version", "status": "ok"}
