from app.core.models import Order


def status() -> dict[str, str]:
    return {"feature": "repeat-order", "status": "ok"}


def repeat_order_items(order: Order) -> list[dict[str, int]]:
    """Retorna os itens do pedido que podem voltar ao carrinho.

    Cada item mantem a mesma quantidade do pedido original,
    desde que o produto tenha estoque suficiente.
    """
    items = []
    for item in order.items:
        if item.quantity <= item.product.stock:
            items.append({"product_id": item.product_id, "quantity": item.quantity})
    return items


def add_items_to_cart(cart: dict[str, int], items: list[dict[str, int]]) -> dict[str, int]:
    """Adiciona os itens ao carrinho, somando com o que ja existe nele."""
    for item in items:
        key = str(item["product_id"])
        cart[key] = cart.get(key, 0) + item["quantity"]
    return cart