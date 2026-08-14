from app.core.types.features import FeatureManifest, MenuItem
from app.features.historico_pedidos.routes import bp

manifest = FeatureManifest(
    id="historico-pedidos",
    name="Historico Pedidos",
    blueprint=bp,
    menu=MenuItem(label="Historico Pedidos", endpoint="historico_pedidos.page", order=50),
    slots=[],
)
