from flask import url_for

from app.core.types.features import FeatureManifest, SlotContribution
from app.features.recently_viewed.routes import recently_viewed_bp


def _view_details_link(product, **_context) -> str:
    url = url_for("recently_viewed.product_detail", product_id=product.id)
    return f'<a class="button-link" href="{url}">Ver detalhes</a>'


manifest = FeatureManifest(
    id="recently_viewed",
    name="Produtos vistos recentemente",
    blueprint=recently_viewed_bp,
    slots=[SlotContribution(slot="PRODUCT_CARD", renderer=_view_details_link)],
)