from types import SimpleNamespace

from app.features.desconto_por_categoria.service import (
    DISCOUNT_CATEGORY,
    cart_discount,
    discounted_price,
    has_discount,
)


def test_categoria_definida_recebe_desconto():
    assert has_discount(DISCOUNT_CATEGORY) is True
    assert discounted_price(100.0, DISCOUNT_CATEGORY) == 90.0


def test_outras_categorias_nao_recebem_desconto():
    for category in ["Bebidas", "Limpeza", "Higiene"]:
        assert has_discount(category) is False
        assert discounted_price(100.0, category) == 100.0


def test_desconto_no_carrinho_so_conta_categoria_definida():
    arroz = SimpleNamespace(price=20.0, category="Mercearia")
    cafe = SimpleNamespace(price=15.0, category="Bebidas")
    items = [
        {"product": arroz, "quantity": 2},
        {"product": cafe, "quantity": 1},
    ]

    assert cart_discount(items) == 4.0
