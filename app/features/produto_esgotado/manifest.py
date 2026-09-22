from app.core.types.features import FeatureManifest, SlotContribution
from app.features.produto_esgotado.service import OUT_OF_STOCK_LABEL, is_out_of_stock


def render_out_of_stock_badge(product=None, **_context) -> str:
    if product is None or not is_out_of_stock(product):
        return ""
    return f'<span class="badge badge-out-of-stock">{OUT_OF_STOCK_LABEL}</span>'


manifest = FeatureManifest(
    id="produto-esgotado",
    name="Produto Esgotado",
    slots=[SlotContribution(slot="PRODUCT_CARD", renderer=render_out_of_stock_badge)],
)
