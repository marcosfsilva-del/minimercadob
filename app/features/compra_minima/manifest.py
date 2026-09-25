from app.core.types.features import FeatureManifest, MenuItem
from app.features.compra_minima.routes import bp

manifest = FeatureManifest(
    id="compra-minima",
    name="Compra Minima",
    blueprint=bp,
    menu=MenuItem(label="Compra Minima", endpoint="compra_minima.page", order=50),
    slots=[],
)
