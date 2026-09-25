from app.core.types.features import FeatureManifest, MenuItem, SlotContribution
from app.features.product_search.routes import bp
from app.features.product_search.routes import render_toolbar

manifest = FeatureManifest(
    id="product-search",
    name="Product Search",
    blueprint=bp,
    menu=MenuItem(label="Product Search", endpoint="product_search.page", order=50),
    slots=[SlotContribution(slot="PRODUCT_LIST_TOOLBAR", renderer=render_toolbar)],
)
