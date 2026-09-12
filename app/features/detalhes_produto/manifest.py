from flask import url_for

from app.core.types.features import FeatureManifest, SlotContribution
from app.features.detalhes_produto.routes import bp


def link_detalhes(product=None, **_context) -> str:
    if product is None:
        return ""
    url = url_for("detalhes_produto.page", product_id=product.id)
    return f'<a class="button-link" href="{url}">Ver detalhes</a>'


manifest = FeatureManifest(
    id="detalhes-produto",
    name="Detalhes Produto",
    blueprint=bp,
    menu=None,
    slots=[SlotContribution(slot="PRODUCT_CARD", renderer=link_detalhes)],
)
