from app.core.types.features import FeatureManifest, MenuItem
from app.features.regra_leve3_pague2.routes import bp

manifest = FeatureManifest(
    id="regra-leve3-pague2",
    name="Regra Leve3 Pague2",
    blueprint=bp,
    menu=MenuItem(label="Regra Leve3 Pague2", endpoint="regra_leve3_pague2.page", order=50),
    slots=[],
)
