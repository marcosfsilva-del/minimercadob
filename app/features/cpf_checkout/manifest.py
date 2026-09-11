from flask import render_template

from app.core.types.features import FeatureManifest, SlotContribution
from app.features.cpf_checkout.routes import cpf_bp


def campo_cpf(**_context):
    return render_template("campo_cpf.html")


manifest = FeatureManifest(
    id="cpf-checkout",
    name="cpf no checkout",
    blueprint=cpf_bp,
    slots=[SlotContribution(slot="CHECKOUT_FORM", renderer=campo_cpf)],
)
