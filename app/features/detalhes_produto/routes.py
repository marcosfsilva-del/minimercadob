from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.core.database import session_scope
from app.features.detalhes_produto.service import get_product

bp = Blueprint("detalhes_produto", __name__, url_prefix="/produto", template_folder="templates")


def _nao_encontrado(product_id: int):
    return render_template("detalhes-produto/nao-encontrado.html", product_id=product_id), 404


@bp.get("/<int:product_id>")
def page(product_id: int):
    with session_scope() as db:
        product = get_product(db, product_id)

    if product is None:
        return _nao_encontrado(product_id)
    return render_template("detalhes-produto/produto.html", product=product)


@bp.post("/<int:product_id>/adicionar")
def add_to_cart(product_id: int):
    with session_scope() as db:
        product = get_product(db, product_id)

    if product is None:
        return _nao_encontrado(product_id)

    cart = session.setdefault("cart", {})
    key = str(product.id)
    cart[key] = cart.get(key, 0) + 1
    session.modified = True
    flash(f"{product.name} adicionado ao carrinho.")

    if request.form.get("destino") == "carrinho":
        return redirect(url_for("web.cart"))
    return redirect(url_for("detalhes_produto.page", product_id=product.id))
