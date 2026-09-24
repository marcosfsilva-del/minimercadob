from app.core.types.features import FeatureManifest, MenuItem
from app.features.desconto_por_categoria.routes import bp

manifest = FeatureManifest(
    id="desconto-por-categoria",
    name="Desconto Por Categoria",
    blueprint=bp,
    menu=MenuItem(
        label="Desconto Por Categoria", endpoint="desconto_por_categoria.page", order=50
    ),
    slots=[],
)
