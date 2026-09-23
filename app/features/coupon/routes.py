from flask import Blueprint, flash, redirect, request, session, url_for

from app.features.coupon.service import find_coupon

coupon_bp = Blueprint(
    "coupon",
    __name__,
    url_prefix="/coupon",
    template_folder="templates",
)


@coupon_bp.post("/apply")
def apply():
    code = request.form.get("coupon", "").strip().upper()
    if find_coupon(code) is None:
        session.pop("coupon", None)
        flash("Cupom não encontrado. Confira o código e tente novamente.")
    else:
        session["coupon"] = code
        flash(f"Cupom {code} aplicado.")
    return redirect(url_for("web.cart"))
