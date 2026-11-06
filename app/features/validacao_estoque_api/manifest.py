from app.core.types.features import FeatureManifest, MenuItem
from app.features.validacao_estoque_api.routes import bp

manifest = FeatureManifest(
    id="validacao-estoque-api",
    name="Validacao Estoque Api",
    blueprint=bp,
    menu=MenuItem(label="Validacao Estoque Api", endpoint="validacao_estoque_api.page", order=50),
    slots=[],
)
