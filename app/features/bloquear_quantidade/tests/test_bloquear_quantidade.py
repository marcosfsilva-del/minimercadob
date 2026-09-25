from app.features.bloquear_quantidade.service import (
    status,
    validar_quantidade_estoque,
)


def test_status():
    res = status()
    assert res["status"] == "active"


def test_bloquear_quantidade_acima_do_estoque():
    # Prova o requisito da Issue #116: bloqueia quando quantidade > estoque
    assert validar_quantidade_estoque(quantidade=15, estoque=10) is False


def test_permitir_quantidade_dentro_do_estoque():
    # Confirma que quantidades validas sao permitidas
    assert validar_quantidade_estoque(quantidade=5, estoque=10) is True