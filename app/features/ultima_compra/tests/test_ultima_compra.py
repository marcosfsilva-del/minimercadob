from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.models import Order
from app.features.ultima_compra.service import get_last_purchase, last_purchase_to_dict


@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    db = TestingSession()
    yield db
    db.close()


def test_cliente_com_pedidos_mostra_data_da_ultima_compra(session):
    order = Order(
        customer_name="Maria",
        total=100.0,
        created_at=datetime(2026, 1, 10, 12, 0, 0),
    )
    session.add(order)
    session.commit()

    resultado = get_last_purchase(session, "Maria")

    assert resultado is not None
    assert resultado.customer_name == "Maria"
    assert last_purchase_to_dict(resultado)["orderId"] == order.id


def test_cliente_sem_pedidos_mostra_estado_vazio(session):
    resultado = get_last_purchase(session, "Cliente Inexistente")

    assert resultado is None
    assert last_purchase_to_dict(resultado) is None


def test_regra_usa_pedido_mais_recente(session):
    pedido_antigo = Order(
        customer_name="Joao",
        total=50.0,
        created_at=datetime(2026, 1, 1, 9, 0, 0),
    )
    pedido_recente = Order(
        customer_name="Joao",
        total=80.0,
        created_at=datetime(2026, 2, 1, 9, 0, 0),
    )
    session.add_all([pedido_antigo, pedido_recente])
    session.commit()

    resultado = get_last_purchase(session, "Joao")

    assert resultado is not None
    assert resultado.id == pedido_recente.id