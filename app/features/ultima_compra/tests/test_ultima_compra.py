from app.features.ultima_compra.service import status


def test_status():
    assert status() == {"feature": "ultima-compra", "status": "ok"}
