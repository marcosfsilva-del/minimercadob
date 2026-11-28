from app.features.exibir_desconto_por_categoria.service import status


def test_status():
    assert status() == {"feature": "exibir-desconto-por-categoria", "status": "ok"}
