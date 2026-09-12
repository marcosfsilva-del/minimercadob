from flask import Blueprint, render_template

from app.core.database import session_scope
from app.features.detalhes_produto.service import get_product

bp = Blueprint("detalhes_produto", __name__, url_prefix="/produto", template_folder="templates")

@bp.get("/<int:product_id>")
def page(product_id: int):
  with session_scope() as db:
    product = get_product(db, product_id)

    if product is None:
        return (render_template("detalhes-produto/nao-encontrado.html", product_id=product_id),
                404,
            )
    return render_template("detalhes-produto/produto.html", product=product)
