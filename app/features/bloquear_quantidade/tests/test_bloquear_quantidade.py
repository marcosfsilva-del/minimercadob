from app.features.bloquear_quantidade.service import status


def test_status():
    assert status() == {"feature": "bloquear-quantidade", "status": "ok"}
