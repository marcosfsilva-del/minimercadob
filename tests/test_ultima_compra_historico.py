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


def test_cliente_sem_pedidos_retorna_lista_vazia(monkeypatch):
    app = create_app()
    client = app.test_client()

    monkeypatch.setattr(web, "list_orders", lambda db: [])

    response = client.get("/orders")

    assert response.status_code == 200
    assert b"Nenhum pedido registrado ainda." in response.data


def test_cliente_com_pedidos_exibe_pedido(monkeypatch):
    app = create_app()
    client = app.test_client()

    order = Order(
        id=109,
        customer_name="Joao da Silva",
        total=100.00,
        created_at=datetime(2026, 9, 24, 10, 30),
    )

    monkeypatch.setattr(web, "list_orders", lambda db: [order])

    response = client.get("/orders")

    assert response.status_code == 200
    assert b"Joao da Silva" in response.data
    assert b"Pedido #109" in response.data


def test_regra_usa_pedido_mais_recente(monkeypatch):
    app = create_app()
    client = app.test_client()

    pedido_antigo = Order(
        id=110,
        customer_name="Joao da Silva",
        total=80.00,
        created_at=datetime(2026, 9, 20, 10, 30),
    )

    pedido_recente = Order(
        id=111,
        customer_name="Joao da Silva",
        total=120.00,
        created_at=datetime(2026, 9, 25, 14, 30),
    )

    monkeypatch.setattr(
        web,
        "list_orders",
        lambda db: [pedido_recente, pedido_antigo],
    )

    response = client.get("/orders")

    assert response.status_code == 200
    assert response.data.find(b"Pedido #111") < response.data.find(b"Pedido #110")
