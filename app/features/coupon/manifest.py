from flask import render_template

from app.core.types.features import FeatureManifest, SlotContribution
from app.features.coupon.routes import coupon_bp


def coupon_form(**_context) -> str:
    return render_template("coupon_form.html")


manifest = FeatureManifest(
    id="coupon",
    name="Cupom",
    blueprint=coupon_bp,
    slots=[SlotContribution(slot="CART_SUMMARY", renderer=coupon_form)],
)
