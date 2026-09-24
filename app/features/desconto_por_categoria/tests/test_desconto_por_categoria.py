from app.features.desconto_por_categoria.service import status


def test_status():
    assert status() == {"feature": "desconto-por-categoria", "status": "ok"}
