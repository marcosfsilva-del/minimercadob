from flask import Blueprint, flash, redirect, request, url_for

from app.features.coupon.service import find_coupon

coupon_bp = Blueprint(
    "coupon",
    __name__,
    url_prefix="/coupon",
    template_folder="templates",
)


@coupon_bp.post("/apply")
def apply():
    if find_coupon(request.form.get("coupon")) is None:
        flash("Cupom não encontrado. Confira o código e tente novamente.")
    return redirect(url_for("web.cart"))
