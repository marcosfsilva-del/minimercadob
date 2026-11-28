from app.core.types.features import FeatureManifest, SlotContribution
from app.features.exibir_desconto_por_categoria.routes import bp, render_cart_summary

manifest = FeatureManifest(
    id="exibir-desconto-por-categoria",
    name="Exibir Desconto Por Categoria",
    blueprint=bp,
    slots=[SlotContribution(slot="CART_SUMMARY", renderer=render_cart_summary)],
)
