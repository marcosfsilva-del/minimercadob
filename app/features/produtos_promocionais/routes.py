from flask import Blueprint, render_template

from app.core.database import session_scope
from app.features.produtos_promocionais.service import list_promotional_products

bp = Blueprint(
    "produtos_promocionais",
    __name__,
    url_prefix="/produtos-promocionais",
    template_folder="templates",
)


@bp.get("")
def catalog():
    with session_scope() as db:
        products = list_promotional_products(db)
        return render_template("catalog.html", products=products)
