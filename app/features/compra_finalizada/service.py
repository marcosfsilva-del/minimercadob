"""Regras da tela de sucesso exibida depois de finalizar a compra."""

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import Order


@dataclass(frozen=True)
class OrderLine:
    name: str
    quantity: int
    subtotal: float


@dataclass(frozen=True)
class OrderSummary:
    public_code: str
    customer_name: str | None
    total: float
    lines: list[OrderLine]

    @property
    def item_count(self) -> int:
        return sum(line.quantity for line in self.lines)


def normalize_public_code(public_code: str) -> str:
    return public_code.strip().upper()


def latest_order_id(session: Session) -> int | None:
    return session.scalar(select(Order.id).order_by(Order.id.desc()).limit(1))


def find_public_code_created_after(session: Session, previous_id: int | None) -> str | None:
    """Codigo publico do pedido mais recente criado depois de `previous_id`."""
    statement = select(Order.public_code)
    if previous_id is not None:
        statement = statement.where(Order.id > previous_id)
    return session.scalar(statement.order_by(Order.id.desc()).limit(1))


def load_order_summary(session: Session, public_code: str) -> OrderSummary | None:
    """Le o pedido ainda com a sessao aberta para a tela nao depender de lazy load."""
    order = session.scalar(
        select(Order).where(Order.public_code == normalize_public_code(public_code))
    )
    if order is None:
        return None

    return OrderSummary(
        public_code=order.public_code,
        customer_name=order.customer_name,
        total=order.total,
        lines=[
            OrderLine(name=item.product.name, quantity=item.quantity, subtotal=item.subtotal)
            for item in order.items
        ],
    )
