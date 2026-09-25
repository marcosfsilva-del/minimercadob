from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.core.database import session_scope
from app.core.services.market_service import list_products
from app.features.reposicao_estoque.service import (
    list_replenishment_movements,
    replenish_stock,
)

bp = Blueprint(
    "reposicao_estoque",
    __name__,
    url_prefix="/reposicao-estoque",
    template_folder="templates",
)


@bp.get("")
def page():
    with session_scope() as db:
        products = list_products(db)
        movements = list_replenishment_movements(db)
        return render_template(
            "reposicao-estoque.html",
            products=products,
            movements=movements,
        )


@bp.post("")
def confirmar():
    try:
        product_id = int(request.form.get("product_id", ""))
        quantity = int(request.form.get("quantity", ""))
    except ValueError:
        flash("Quantidade deve ser maior que zero.")
        return redirect(url_for("reposicao_estoque.page"))

    try:
        with session_scope() as db:
            replenish_stock(db, product_id, quantity)
    except ValueError as error:
        flash(str(error))
        return redirect(url_for("reposicao_estoque.page"))

    flash("Estoque reposto com sucesso.")
    return redirect(url_for("reposicao_estoque.page"))
