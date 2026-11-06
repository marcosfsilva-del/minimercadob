from types import SimpleNamespace

from app.features.produto_esgotado.manifest import render_out_of_stock_badge
from app.features.produto_esgotado.service import is_out_of_stock


def _product(stock: int):
    return SimpleNamespace(stock=stock)


def test_is_out_of_stock_true_quando_estoque_zero():
    assert is_out_of_stock(_product(0)) is True


def test_is_out_of_stock_true_quando_estoque_negativo():
    assert is_out_of_stock(_product(-1)) is True


def test_is_out_of_stock_false_quando_tem_estoque():
    assert is_out_of_stock(_product(5)) is False


def test_badge_mostra_texto_esgotado_quando_sem_estoque():
    html = render_out_of_stock_badge(product=_product(0))
    assert "esgotado" in html.lower()


def test_badge_vazio_quando_tem_estoque():
    assert render_out_of_stock_badge(product=_product(3)) == ""


def test_badge_vazio_quando_produto_nao_informado():
    assert render_out_of_stock_badge() == ""
