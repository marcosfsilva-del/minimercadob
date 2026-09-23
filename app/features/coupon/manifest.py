from flask import render_template, session

from app.core.types.features import FeatureManifest, SlotContribution
from app.features.coupon.routes import coupon_bp
from app.features.coupon.service import apply_coupon


def coupon_form(total: float = 0.0, **_context) -> str:
    code = session.get("coupon")
    summary = apply_coupon(total, code) if code else None
    return render_template("coupon_form.html", code=code, summary=summary)


manifest = FeatureManifest(
    id="coupon",
    name="Cupom",
    blueprint=coupon_bp,
    slots=[SlotContribution(slot="CART_SUMMARY", renderer=coupon_form)],
)
