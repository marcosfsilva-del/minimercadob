"""Testes de desconto por categoria (requisito 042 - Issue #29)."""

from types import SimpleNamespace

from app.features.desconto_por_categoria.service import (
    DISCOUNT_CATEGORY,
    DISCOUNT_PERCENT,
    cart_discount,
    discounted_price,
    has_discount,
)
from app.features.exibir_desconto_por_categoria.service import cart_summary

ARROZ = SimpleNamespace(price=24.90, category="Mercearia")
CAFE = SimpleNamespace(price=15.90, category="Bebidas")
SABAO = SimpleNamespace(price=12.00, category="Limpeza")


def test_categoria_com_desconto():
    assert DISCOUNT_CATEGORY == "Mercearia"
    assert DISCOUNT_PERCENT == 10
    assert has_discount(" mercearia ") is True
    assert discounted_price(ARROZ.price, ARROZ.category) == 22.41
    assert cart_discount([{"product": ARROZ, "quantity": 2}]) == 4.98


def test_categoria_sem_desconto():
    items = [{"product": CAFE, "quantity": 1}, {"product": SABAO, "quantity": 3}]

    assert discounted_price(CAFE.price, CAFE.category) == 15.90
    assert cart_discount(items) == 0.0


def test_total_final_com_desconto():
    items = [{"product": ARROZ, "quantity": 2}, {"product": CAFE, "quantity": 1}]

    summary = cart_summary(items, total=65.70)

    assert summary["discount"] == 4.98
    assert summary["final_total"] == 60.72


def test_total_final_sem_desconto():
    items = [{"product": CAFE, "quantity": 2}]

    summary = cart_summary(items, total=31.80)

    assert summary["discount"] == 0.0
    assert summary["final_total"] == 31.80


def test_total_final_carrinho_vazio():
    summary = cart_summary([], total=0.0)

    assert summary["final_total"] == 0.0
    assert summary["has_discount"] is False
