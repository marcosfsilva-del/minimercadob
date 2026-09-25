from flask import Blueprint, jsonify, render_template

from app.features.product_search.service import status

bp = Blueprint("product_search", __name__, url_prefix="/product-search", template_folder="templates")


def render_toolbar(**_context) -> str:
    return render_template("product-search-toolbar.html")


@bp.get("")
def page():
    return render_template("product-search.html")


@bp.get("/api")
def api():
    return jsonify(status())
