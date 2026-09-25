from app.features.repeat_order.service import status


def test_status():
    assert status() == {"feature": "repeat-order", "status": "ok"}
