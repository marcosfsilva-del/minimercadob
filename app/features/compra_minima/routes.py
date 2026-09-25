from flask import Blueprint, jsonify, render_template, session

from app.core.database import session_scope
from app.core.services.market_service import list_products
from app.features.compra_minima.service import status_checkout

bp = Blueprint("compra_minima", __name__, url_prefix="/compra-minima", template_folder="templates")


@bp.get("")
def page():
    return render_template("compra-minima.html")


@bp.get("/api")
def api():
    cart = session.get("cart", {})
    with session_scope() as db:
        products = {p.id: p for p in list_products(db)}
    total = sum(products[pid].price * qty for pid, qty in cart.items() if pid in products)
    return jsonify(status_checkout(total))