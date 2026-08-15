from app.core.types.features import FeatureManifest, MenuItem
from app.features.nome_obrigatorio_checkout.routes import bp

manifest = FeatureManifest(
    id="nome-obrigatorio-checkout",
    name="Nome Obrigatorio Checkout",
    blueprint=bp,
    menu=MenuItem(
        label="Nome Obrigatorio Checkout",
        endpoint="nome_obrigatorio_checkout.page",
        order=50,
    ),
    slots=[],
)
