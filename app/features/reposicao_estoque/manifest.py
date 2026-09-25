from app.core.types.features import FeatureManifest, MenuItem
from app.features.reposicao_estoque.routes import bp

manifest = FeatureManifest(
    id="reposicao-estoque",
    name="Reposição de estoque",
    blueprint=bp,
    menu=MenuItem(label="Reposição", endpoint="reposicao_estoque.page", order=60),
    slots=[],
)
