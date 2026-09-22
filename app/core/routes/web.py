from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.core.database import session_scope
from app.core.services.market_service import create_order, list_orders, list_products

web_bp = Blueprint("web", __name__)


def _cart() -> dict[str, int]:
    return session.setdefault("cart", {})


def _cart_items(products):
    cart = _cart()
    product_by_id = {str(product.id): product for product in products}
    items = []
    for product_id, quantity in cart.items():
        product = product_by_id.get(product_id)
        if product:
            items.append({"product": product, "quantity": quantity})
    return items


@web_bp.get("/")
def catalog():
    with session_scope() as db:
        products = list_products(db)
    return render_template("catalog.html", products=products)


@web_bp.post("/cart/add/<int:product_id>")
def add_to_cart(product_id: int):
    cart = _cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session.modified = True
    flash("Produto adicionado ao carrinho.")
    return redirect(url_for("web.catalog"))


@web_bp.get("/cart")
def cart():
    with session_scope() as db:
        products = list_products(db)
    items = _cart_items(products)
    total = sum(item["product"].price * item["quantity"] for item in items)
    return render_template("cart.html", items=items, total=total)


@web_bp.post("/cart/update/<int:product_id>")
def update_cart(product_id: int):
    quantity = max(0, int(request.form.get("quantity", "1")))
    cart = _cart()
    key = str(product_id)
    if quantity == 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    session.modified = True
    return redirect(url_for("web.cart"))


@web_bp.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id: int):
    _cart().pop(str(product_id), None)
    session.modified = True
    return redirect(url_for("web.cart"))


@web_bp.post("/cart/clear")
def clear_cart():
    session["cart"] = {}
    return redirect(url_for("web.cart"))


@web_bp.get("/checkout")
def checkout():
    with session_scope() as db:
        products = list_products(db)
    items = _cart_items(products)
    total = sum(item["product"].price * item["quantity"] for item in items)
    return render_template("checkout.html", items=items, total=total)


@web_bp.post("/checkout")
def finish_checkout():
    with session_scope() as db:
        products = list_products(db)
        items = _cart_items(products)
        payload = [
            {"product_id": item["product"].id, "quantity": item["quantity"]} for item in items
        ]
        create_order(db, payload, request.form.get("customer_name"))

    session["cart"] = {}
    flash("Pedido criado com sucesso.")
    return redirect(url_for("web.orders"))


@web_bp.get("/orders")
def orders():
    with session_scope() as db:
        order_list = list_orders(db)
    return render_template("orders.html", orders=order_list)
