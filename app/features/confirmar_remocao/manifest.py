from app.core.types.features import FeatureManifest, MenuItem
from app.features.confirmar_remocao.routes import bp

manifest = FeatureManifest(
    id="confirmar-remocao",
    name="Confirmar Remocao",
    blueprint=bp,
    menu=MenuItem(label="Confirmar Remocao", endpoint="confirmar_remocao.page", order=50),
    slots=[],
)
