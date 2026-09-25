from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.models import InventoryMovement, Product

MOVEMENT_TYPE = "REPOSICAO"


def status() -> dict[str, str]:
    return {"feature": "reposicao-estoque", "status": "ok"}


def replenish_stock(session: Session, product_id: int, quantity: int) -> InventoryMovement:
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        raise ValueError("Quantidade deve ser maior que zero.")

    product = session.get(Product, product_id)
    if product is None:
        raise ValueError("Produto não encontrado.")

    product.stock += quantity
    movement = InventoryMovement(
        product_id=product.id,
        type=MOVEMENT_TYPE,
        quantity=quantity,
    )
    session.add(movement)
    session.flush()
    return movement


def list_replenishment_movements(session: Session) -> list[InventoryMovement]:
    statement = (
        select(InventoryMovement)
        .options(joinedload(InventoryMovement.product))
        .where(InventoryMovement.type == MOVEMENT_TYPE)
        .order_by(InventoryMovement.created_at.desc(), InventoryMovement.id.desc())
    )
    return list(session.scalars(statement).unique())
