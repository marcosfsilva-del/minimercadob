from app.core.types.features import FeatureManifest, MenuItem
from app.features.exibir_desconto_por_categoria.routes import bp

manifest = FeatureManifest(
    id="exibir-desconto-por-categoria",
    name="Exibir Desconto Por Categoria",
    blueprint=bp,
    menu=MenuItem(label="Exibir Desconto Por Categoria", endpoint="exibir_desconto_por_categoria.page", order=50),
    slots=[],
)
