from app.core.types.features import FeatureManifest, SlotContribution
from app.features.cart_subtotal.service import (
    render_cart_item_subtotal,
    render_cart_summary_script,
)

manifest = FeatureManifest(
    id="cart-subtotal",
    name="Atualizacao de subtotal do carrinho",
    slots=[
        SlotContribution(slot="CART_ITEM", renderer=render_cart_item_subtotal),
        SlotContribution(slot="CART_SUMMARY", renderer=render_cart_summary_script),
    ],
)
