import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.models import Product
from app.core.services.market_service import create_order, order_to_dict


def test_create_order_rejects_empty_items():
    with pytest.raises(ValueError, match="pelo menos um item"):
        create_order(session=None, items=[])  # type: ignore[arg-type]


def _session_with_product():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    product = Product(
        name="Arroz",
        description="Arroz branco",
        category="Mercearia",
        price=10.0,
        stock=5,
        promotional=False,
    )
    session.add(product)
    session.flush()
    return session, product


def test_create_order_with_pickup_does_not_require_address():
    session, product = _session_with_product()

    order = create_order(
        session,
        [{"product_id": product.id, "quantity": 1}],
        delivery_method="retirada",
    )

    assert order.delivery_method == "retirada"
    assert order.delivery_address is None


def test_create_order_with_delivery_saves_address():
    session, product = _session_with_product()

    order = create_order(
        session,
        [{"product_id": product.id, "quantity": 1}],
        delivery_method="entrega",
        delivery_address=" Rua A, 123 ",
    )

    assert order.delivery_method == "entrega"
    assert order.delivery_address == "Rua A, 123"

    serialized = order_to_dict(order)
    assert serialized["deliveryMethod"] == "entrega"
    assert serialized["deliveryAddress"] == "Rua A, 123"


def test_create_order_with_delivery_requires_address():
    session, product = _session_with_product()

    with pytest.raises(ValueError, match="Endereço é obrigatório para entrega"):
        create_order(
            session,
            [{"product_id": product.id, "quantity": 1}],
            delivery_method="entrega",
        )
