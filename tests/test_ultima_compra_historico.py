from datetime import datetime

from app.core import create_app
from app.core.models import Order
from app.core.routes import web


def test_historico_exibe_dados_da_ultima_compra(monkeypatch):
    app = create_app()
    client = app.test_client()

    order = Order(
        id=108,
        customer_name="Joao da Silva",
        total=150.50,
        created_at=datetime(2026, 9, 25, 14, 30),
    )

    monkeypatch.setattr(web, "list_orders", lambda db: [order])

    response = client.get("/orders")

    assert response.status_code == 200
    assert b"Joao da Silva" in response.data
    assert b"25/09/2026 14:30" in response.data
    assert b"/orders/108" in response.data


def test_detalhes_exibem_dados_da_compra(monkeypatch):
    app = create_app()
    client = app.test_client()

    order = Order(
        id=108,
        customer_name="Joao da Silva",
        total=150.50,
        created_at=datetime(2026, 9, 25, 14, 30),
    )

    monkeypatch.setattr(web, "get_order", lambda db, order_id: order)

    response = client.get("/orders/108")

    assert response.status_code == 200
    assert b"Joao da Silva" in response.data
    assert b"25/09/2026 14:30" in response.data
    assert b"150,50" in response.data

