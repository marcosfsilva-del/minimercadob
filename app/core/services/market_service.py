from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import InventoryMovement, Order, OrderItem, Product


def list_products(session: Session) -> list[Product]:
    return list(session.scalars(select(Product).order_by(Product.name)))


def list_orders(session: Session) -> list[Order]:
    return list(session.scalars(select(Order).order_by(Order.created_at.desc())))


def create_order(
    session: Session,
    items: list[dict[str, int]],
    customer_name: str | None = None,
    delivery_method: str = "retirada",
    delivery_address: str | None = None,
) -> Order:
    if not items:
        raise ValueError("Pedido precisa ter pelo menos um item.")

    if delivery_method not in {"retirada", "entrega"}:
        raise ValueError("Forma de entrega inválida.")

    normalized_address = delivery_address.strip() if delivery_address else None
    if delivery_method == "entrega" and not normalized_address:
        raise ValueError("Endereço é obrigatório para entrega.")

    product_ids = [item["product_id"] for item in items]
    products = session.scalars(select(Product).where(Product.id.in_(product_ids))).all()
    product_by_id = {product.id: product for product in products}

    order_items: list[OrderItem] = []
    total = 0.0

    for item in items:
        product = product_by_id.get(item["product_id"])
        quantity = item["quantity"]

        if product is None:
            raise ValueError(f"Produto não encontrado: {item['product_id']}")
        if quantity < 1:
            raise ValueError("Quantidade deve ser maior que zero.")
        if quantity > product.stock:
            raise ValueError(f"Estoque insuficiente para {product.name}.")

        subtotal = product.price * quantity
        total += subtotal
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
                subtotal=subtotal,
            )
        )

    order = Order(
        customer_name=customer_name or None,
        delivery_method=delivery_method,
        delivery_address=normalized_address if delivery_method == "entrega" else None,
        total=total,
        items=order_items,
    )
    session.add(order)

    for item in items:
        product = product_by_id[item["product_id"]]
        product.stock -= item["quantity"]
        session.add(
            InventoryMovement(product_id=product.id, type="SALE", quantity=item["quantity"])
        )

    session.flush()
    return order


def product_to_dict(product: Product) -> dict[str, object]:
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": product.price,
        "stock": product.stock,
        "promotional": product.promotional,
    }


def order_to_dict(order: Order) -> dict[str, object]:
    return {
        "id": order.id,
        "customerName": order.customer_name,
        "deliveryMethod": order.delivery_method,
        "deliveryAddress": order.delivery_address,
        "total": order.total,
        "createdAt": order.created_at.isoformat(),
        "items": [
            {
                "id": item.id,
                "productId": item.product_id,
                "quantity": item.quantity,
                "unitPrice": item.unit_price,
                "subtotal": item.subtotal,
                "product": product_to_dict(item.product),
            }
            for item in order.items
        ],
    }
