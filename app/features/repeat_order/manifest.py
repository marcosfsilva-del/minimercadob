from app.core.types.features import FeatureManifest, MenuItem
from app.features.repeat_order.routes import bp

manifest = FeatureManifest(
    id="repeat-order",
    name="Repeat Order",
    blueprint=bp,
    menu=MenuItem(label="Repeat Order", endpoint="repeat_order.page", order=50),
    slots=[],
)
