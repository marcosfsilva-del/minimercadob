from types import SimpleNamespace

from app.core import create_app
from app.features.exibir_desconto_por_categoria.routes import render_cart_summary
from app.features.exibir_desconto_por_categoria.service import cart_summary


def _items_com_desconto():
    arroz = SimpleNamespace(price=20.0, category="Mercearia")
    cafe = SimpleNamespace(price=15.0, category="Bebidas")
    return [{"product": arroz, "quantity": 2}, {"product": cafe, "quantity": 1}], 55.0


def _items_sem_desconto():
    cafe = SimpleNamespace(price=15.0, category="Bebidas")
    return [{"product": cafe, "quantity": 2}], 30.0


def test_resumo_calcula_desconto_e_total_final():
    items, total = _items_com_desconto()

    summary = cart_summary(items, total)

    assert summary["subtotal"] == 55.0
    assert summary["discount"] == 4.0
    assert summary["final_total"] == 51.0
    assert summary["has_discount"] is True


def test_resumo_sem_desconto_mantem_total():
    items, total = _items_sem_desconto()

    summary = cart_summary(items, total)

    assert summary["discount"] == 0.0
    assert summary["final_total"] == 30.0
    assert summary["has_discount"] is False


def test_resumo_exibe_valor_do_desconto_e_total_final():
    items, total = _items_com_desconto()

    with create_app().test_request_context():
        html = render_cart_summary(items=items, total=total)

    assert "Desconto Mercearia (10%)" in html
    assert "R$ 4,00" in html
    assert "Total final" in html
    assert "R$ 51,00" in html


def test_resumo_sem_desconto_nao_exibe_linha_de_desconto():
    items, total = _items_sem_desconto()

    with create_app().test_request_context():
        html = render_cart_summary(items=items, total=total)

    assert "Desconto" not in html
    assert "Total final" in html
    assert "R$ 30,00" in html
