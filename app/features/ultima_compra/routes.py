from flask import Blueprint, jsonify, render_template, request

from app.core.database import session_scope
from app.features.ultima_compra.service import get_last_purchase, last_purchase_to_dict

bp = Blueprint("ultima_compra", __name__, url_prefix="/ultima-compra", template_folder="templates")


@bp.get("")
def page():
    return render_template("ultima-compra.html")


@bp.get("/api")
def api():
    customer_name = request.args.get("customer_name", "")
    with session_scope() as db:
        order = get_last_purchase(db, customer_name)
        result = last_purchase_to_dict(order)
    return jsonify(result)