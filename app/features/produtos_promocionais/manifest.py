from flask import render_template, request

from app.core.models import Product
from app.core.types.features import FeatureManifest, SlotContribution
from app.features.produtos_promocionais.routes import bp


def render_toolbar(*, products: list[Product]) -> str:
    return render_template(
        "produtos_promocionais/toolbar.html",
        promotions_active=request.endpoint == "produtos_promocionais.catalog",
        products=products,
    )


manifest = FeatureManifest(
    id="produtos-promocionais",
    name="Produtos promocionais",
    blueprint=bp,
    slots=[SlotContribution(slot="PRODUCT_LIST_TOOLBAR", renderer=render_toolbar)],
)
