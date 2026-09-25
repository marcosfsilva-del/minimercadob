from app.core.types.features import FeatureManifest
from app.features.compra_finalizada.routes import bp

manifest = FeatureManifest(
    id="compra-finalizada",
    name="Compra Finalizada",
    blueprint=bp,
    menu=None,
    slots=[],
)
