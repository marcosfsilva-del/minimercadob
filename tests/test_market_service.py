import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.database import Base
from app.core.models import Order, Product
from app.core.services.market_service import create_order


def test_create_order_rejects_empty_items():
    with pytest.raises(ValueError, match="pelo menos um item"):
        create_order(session=None, items=[])  # type: ignore[arg-type]


def test_create_order_rejects_empty_customer_name():
    """Issue #43: o checkout exige nome; sem nome o pedido nem chega a ser criado."""
    items = [{"product_id": 1, "quantity": 1}]
    with pytest.raises(ValueError, match="nome do cliente"):
        create_order(session=None, items=items, customer_name="   ")  # type: ignore[arg-type]


def test_create_order_saves_customer_name():
    """Issue #43: o pedido salvo no banco contém o nome informado (sem espaços nas pontas)."""
    engine = create_engine("sqlite://")  # banco em memória, só para este teste
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        product = Product(
            name="Arroz", description="Pacote 5 kg", category="Mercearia", price=25.0, stock=10
        )
        db.add(product)
        db.flush()

        order = create_order(db, [{"product_id": product.id, "quantity": 1}], "  Maria Silva  ")
        db.commit()

        saved_name = db.scalar(select(Order.customer_name).where(Order.id == order.id))
        assert saved_name == "Maria Silva"
