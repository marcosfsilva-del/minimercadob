from flask import Blueprint, jsonify, request

from app.core.config import settings
from app.core.database import session_scope
from app.core.services.market_service import (
    create_order,
    list_orders,
    list_products,
    order_to_dict,
    product_to_dict,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("")
def index():
    return jsonify({"name": "DevOps Market", "status": "online"})


@api_bp.get("/health")
def health():
    return jsonify(
        {"status": "ok", "version": settings.app_version, "commit": settings.commit_sha}
    )


@api_bp.get("/ready")
def ready():
    return jsonify({"status": "ready"})


@api_bp.get("/products")
def products():
    with session_scope() as db:
        return jsonify([product_to_dict(product) for product in list_products(db)])


@api_bp.get("/orders")
def orders():
    with session_scope() as db:
        return jsonify([order_to_dict(order) for order in list_orders(db)])


@api_bp.post("/orders")
def create_order_api():
    data = request.get_json(silent=True) or {}
    items = [
        {"product_id": int(item["productId"]), "quantity": int(item["quantity"])}
        for item in data.get("items", [])
    ]

    try: #adciona um try pra capturar o erro
        with session_scope() as db:
            order = create_order(db, items, data.get("customerName"))
            return jsonify(order_to_dict(order)), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

# @api_bp.post("/orders") versão antiga
# def create_order_api():
#     data = request.get_json(silent=True) or {}
#     items = [
#         {"product_id": int(item["productId"]), "quantity": int(item["quantity"])}
#         for item in data.get("items", [])
#     ]
#     with session_scope() as db:
#         order = create_order(db, items, data.get("customerName"))
#         return jsonify(order_to_dict(order)), 201
