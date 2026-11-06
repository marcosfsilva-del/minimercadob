from types import SimpleNamespace

from app.features.cart_subtotal.manifest import manifest
from app.features.cart_subtotal.service import (
    render_cart_item_subtotal,
    render_cart_summary_script,
)


def test_cart_item_renderer_includes_quantity_subtotal():
    item = {"product": SimpleNamespace(price=12.5), "quantity": 3}

    rendered = render_cart_item_subtotal(item=item)

    assert 'data-cart-unit-price="12.50"' in rendered
    assert "Subtotal: <span data-cart-subtotal>R$ 37,50</span>" in rendered


def test_cart_summary_renderer_recalculates_subtotals_and_total():
    rendered = render_cart_summary_script()

    assert 'addEventListener("input", updateCartTotals)' in rendered
    assert 'data-cart-subtotal' in rendered
    assert 'document.querySelector(".summary .total")' in rendered
    assert "Number(priceElement.dataset.cartUnitPrice)" in rendered


def test_manifest_registers_cart_slots():
    assert {contribution.slot for contribution in manifest.slots} == {
        "CART_ITEM",
        "CART_SUMMARY",
    }
