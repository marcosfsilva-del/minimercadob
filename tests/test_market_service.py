import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.models import Customer, Order
from app.core.services.market_service import create_order, total_spent_by_customer


@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_create_order_rejects_empty_items():
    with pytest.raises(ValueError, match="pelo menos um item"):
        create_order(session=None, items=[])  # type: ignore[arg-type]


def test_total_spent_by_customer_sums_orders(session):
    customer = Customer(name="Maria Silva")
    session.add(customer)
    session.add(Order(customer_name="Maria Silva", total=50.0))
    session.add(Order(customer_name="Maria Silva", total=30.0))
    session.commit()

    total = total_spent_by_customer(session, customer.id)

    assert total == 80.0


def test_total_spent_by_customer_without_orders_is_zero(session):
    customer = Customer(name="Joao Souza")
    session.add(customer)
    session.commit()

    total = total_spent_by_customer(session, customer.id)

    assert total == 0.0


def test_total_spent_by_customer_raises_for_unknown_customer(session):
    with pytest.raises(ValueError, match="não encontrado"):
        total_spent_by_customer(session, 999)