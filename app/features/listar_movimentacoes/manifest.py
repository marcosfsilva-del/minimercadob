from app.core.types.features import FeatureManifest, MenuItem
from app.features.listar_movimentacoes.routes import bp

manifest = FeatureManifest(
    id="listar-movimentacoes",
    name="Movimentações",
    blueprint=bp,
    menu=MenuItem(label="Movimentações", endpoint="listar_movimentacoes.page", order=50),
    slots=[],
)
