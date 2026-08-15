from app.features.nome_obrigatorio_checkout.service import status


def test_status():
    assert status() == {"feature": "nome-obrigatorio-checkout", "status": "ok"}
