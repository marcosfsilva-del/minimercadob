from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.models import InventoryMovement

TYPE_LABELS = {"SALE": "Venda"}


def type_label(movement_type: str) -> str:
    return TYPE_LABELS.get(movement_type, movement_type)


def list_movements(session: Session) -> list[InventoryMovement]:
    return list(
        session.scalars(
            select(InventoryMovement)
            .options(joinedload(InventoryMovement.product))
            .order_by(InventoryMovement.created_at.desc(), InventoryMovement.id.desc())
        )
    )
