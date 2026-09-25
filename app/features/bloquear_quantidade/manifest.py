from app.core.types.features import FeatureManifest, MenuItem
from app.features.bloquear_quantidade.routes import bp

manifest = FeatureManifest(
    id="bloquear-quantidade",
    name="Bloquear Quantidade",
    blueprint=bp,
    menu=MenuItem(label="Bloquear Quantidade", endpoint="bloquear_quantidade.page", order=50),
    slots=[],
)
