from app.features.validacao_estoque_api.service import status


def test_status():
    assert status() == {"feature": "validacao-estoque-api", "status": "ok"}
