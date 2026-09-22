from app.features.confirmar_remocao.service import status


def test_status():
    assert status() == {"feature": "confirmar-remocao", "status": "ok"}
