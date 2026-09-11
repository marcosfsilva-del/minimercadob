from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.core.database import session_scope
from app.core.routes.web import _cart_items
from app.core.services.market_service import list_products
from app.features.cpf_checkout.service import criar_pedido_com_cpf

cpf_bp = Blueprint("cpf_checkout", __name__, template_folder="templates")


@cpf_bp.before_app_request
def finalizar_com_cpf():
    if request.endpoint != "web.finish_checkout" or request.method != "POST":
        return None

    try:
        with session_scope() as db:
            items = _cart_items(list_products(db))
            payload = [
                {"product_id": item["product"].id, "quantity": item["quantity"]}
                for item in items
            ]
            criar_pedido_com_cpf(
                db, payload, request.form.get("customer_name"), request.form.get("cpf", "")
            )
    except ValueError as erro:
        with session_scope() as db:
            items = _cart_items(list_products(db))
        total = sum(item["product"].price * item["quantity"] for item in items)
        flash(str(erro).lower())
        return render_template("checkout.html", items=items, total=total), 400

    session["cart"] = {}
    flash("pedido criado com sucesso.")
    return redirect(url_for("web.orders"))
