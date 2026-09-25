from flask import Blueprint, flash, jsonify, redirect, render_template, session, url_for

from app.core.database import session_scope
from app.core.models import Order
from app.core.services.market_service import list_orders
from app.features.repeat_order.service import add_items_to_cart, repeat_order_items, status

bp = Blueprint("repeat_order", __name__, url_prefix="/repeat-order", template_folder="templates")


@bp.get("")
def page():
    # A tela e montada DENTRO do "with", enquanto a conexao com o banco
    # esta aberta, para os itens de cada pedido poderem ser carregados.
    with session_scope() as db:
        orders = list_orders(db)
        return render_template("repeat-order.html", orders=orders)


@bp.get("/api")
def api():
    return jsonify(status())


@bp.post("/<int:order_id>")
def repeat(order_id: int):
    with session_scope() as db:
        order = db.get(Order, order_id)
        if order is None:
            flash("Pedido nao encontrado.")
            return redirect(url_for("repeat_order.page"))
        items = repeat_order_items(order)

    cart = session.setdefault("cart", {})
    add_items_to_cart(cart, items)
    session.modified = True

    if items:
        flash(f"Itens do pedido #{order_id} adicionados ao carrinho.")
    else:
        flash("Nenhum item deste pedido tem estoque disponivel.")
    return redirect(url_for("web.cart"))