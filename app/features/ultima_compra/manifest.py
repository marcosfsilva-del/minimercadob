from app.core.types.features import FeatureManifest, MenuItem
from app.features.ultima_compra.routes import bp

manifest = FeatureManifest(
    id="ultima-compra",
    name="Ultima Compra",
    blueprint=bp,
    menu=MenuItem(label="Ultima Compra", endpoint="ultima_compra.page", order=50),
    slots=[],
)
