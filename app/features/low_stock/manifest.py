from app.core.types.features import FeatureManifest, MenuItem, SlotContribution
from app.features.low_stock.routes import bp
from app.features.low_stock.service import render_product_card_warning, render_toolbar_button

manifest = FeatureManifest(
    id="low-stock",
    name="Estoque Baixo",
    blueprint=bp,
    menu=MenuItem(label="Estoque Baixo", endpoint="low_stock.page", order=60),
    slots=[
        SlotContribution(slot="PRODUCT_CARD", renderer=render_product_card_warning),
        SlotContribution(slot="PRODUCT_LIST_TOOLBAR", renderer=render_toolbar_button),
    ],
)