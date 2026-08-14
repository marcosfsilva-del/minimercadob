from app.features.historico_pedidos.service import status


def test_status():
    assert status() == {"feature": "historico-pedidos", "status": "ok"}
