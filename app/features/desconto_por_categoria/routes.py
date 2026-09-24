from flask import Blueprint, jsonify, render_template

from app.core.database import session_scope
from app.core.services.market_service import list_products
from app.features.desconto_por_categoria.service import discounted_price, has_discount, rule

bp = Blueprint(
    "desconto_por_categoria",
    __name__,
    url_prefix="/desconto-por-categoria",
    template_folder="templates",
)


@bp.get("")
def page():
    with session_scope() as db:
        products = list_products(db)
    rows = [
        {
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "final_price": discounted_price(product.price, product.category),
            "has_discount": has_discount(product.category),
        }
        for product in products
    ]
    return render_template("desconto-por-categoria.html", rule=rule(), rows=rows)


@bp.get("/api")
def api():
    return jsonify(rule())
