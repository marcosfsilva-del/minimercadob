from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import Order


def get_last_purchase(session: Session, customer_name: str) -> Order | None:
    """Retorna o pedido mais recente do cliente informado.

    Retorna None quando o cliente nao possui nenhum pedido.
    """
    stmt = (
        select(Order)
        .where(Order.customer_name == customer_name)
        .order_by(Order.created_at.desc())
        .limit(1)
    )
    return session.scalars(stmt).first()


def last_purchase_to_dict(order: Order | None) -> dict[str, object] | None:
    """Serializa o pedido mais recente para uso em rotas/templates."""
    if order is None:
        return None
    return {
        "orderId": order.id,
        "createdAt": order.created_at.isoformat(),
        "total": order.total,
    }