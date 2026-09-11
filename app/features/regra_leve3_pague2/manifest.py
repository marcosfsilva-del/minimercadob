from flask import render_template

from app.core.types.features import FeatureManifest, MenuItem, SlotContribution
from app.features.regra_leve3_pague2.routes import bp
from app.features.regra_leve3_pague2.service import (
    calcular_promocao,
    produto_elegivel,
    unidades_gratuitas,
)


def resumo_economia(items=None, total=None, **_context) -> str:
    """Mostra a economia no resumo do carrinho, so quando a regra se aplica."""
    promocao = calcular_promocao(items or [])
    if not promocao["aplicou"]:
        return ""
    return render_template("leve3-pague2-resumo.html", promocao=promocao)


def selo_item(item=None, **_context) -> str:
    """Marca no item do carrinho quantas unidades sairam de graca."""
    if not item:
        return ""
    gratis = unidades_gratuitas(int(item["quantity"])) if produto_elegivel(item["product"]) else 0
    if gratis <= 0:
        return ""
    return render_template("leve3-pague2-item.html", gratis=gratis)


manifest = FeatureManifest(
    id="regra-leve3-pague2",
    name="Regra Leve3 Pague2",
    blueprint=bp,
    menu=MenuItem(label="Leve 3 Pague 2", endpoint="regra_leve3_pague2.page", order=50),
    slots=[
        SlotContribution(slot="CART_SUMMARY", renderer=resumo_economia),
        SlotContribution(slot="CHECKOUT_FORM", renderer=resumo_economia),
        SlotContribution(slot="CART_ITEM", renderer=selo_item),
    ],
)
