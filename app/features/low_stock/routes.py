from flask import Blueprint, jsonify, render_template

from app.core.database import session_scope
from app.core.services.market_service import list_products, product_to_dict
from app.features.low_stock.service import filter_low_stock

bp = Blueprint("low_stock", __name__, url_prefix="/low-stock", template_folder="templates")


@bp.get("")
def page():
    with session_scope() as db:
        products = list_products(db)
    low_stock_products = filter_low_stock(products)
    return render_template("low-stock.html", products=low_stock_products)


@bp.get("/api")
def api():
    with session_scope() as db:
        products = list_products(db)
    low_stock_products = filter_low_stock(products)
    return jsonify([product_to_dict(p) for p in low_stock_products])