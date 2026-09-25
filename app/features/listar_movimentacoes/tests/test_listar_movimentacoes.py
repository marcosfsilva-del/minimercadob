from datetime import datetime

import pytest
from sqlalchemy import delete

from app.core import create_app
from app.core.database import init_database, session_scope
from app.core.models import InventoryMovement, Product
from app.features.listar_movimentacoes.service import list_movements, type_label


@pytest.fixture(autouse=True)
def clean_movements():
    init_database()
    with session_scope() as db:
        db.execute(delete(InventoryMovement))
    yield
    with session_scope() as db:
        db.execute(delete(InventoryMovement))
        db.execute(delete(Product).where(Product.name.like("Teste Movimentacao%")))


@pytest.fixture
def client():
    return create_app().test_client()


def _create_movement(product_name: str, quantity: int, created_at: datetime) -> None:
    with session_scope() as db:
        product = Product(
            name=product_name,
            description="Produto de teste",
            category="Teste",
            price=1.0,
            stock=10,
        )
        db.add(product)
        db.flush()
        db.add(
            InventoryMovement(
                product_id=product.id,
                type="SALE",
                quantity=quantity,
                created_at=created_at,
            )
        )


def test_list_movements_empty():
    with session_scope() as db:
        assert list_movements(db) == []


def test_list_movements_orders_most_recent_first():
    _create_movement("Teste Movimentacao Antiga", 1, datetime(2026, 1, 1, 10, 0))
    _create_movement("Teste Movimentacao Recente", 2, datetime(2026, 2, 1, 10, 0))

    with session_scope() as db:
        names = [movement.product.name for movement in list_movements(db)]

    assert names == ["Teste Movimentacao Recente", "Teste Movimentacao Antiga"]


def test_type_label_translates_sale():
    assert type_label("SALE") == "Venda"


def test_type_label_keeps_unknown_type():
    assert type_label("ADJUSTMENT") == "ADJUSTMENT"


def test_page_renders_empty_state(client):
    response = client.get("/listar-movimentacoes")

    assert response.status_code == 200
    assert "Nenhuma movimentação registrada ainda.".encode() in response.data


def test_page_lists_product_type_quantity_date(client):
    _create_movement("Teste Movimentacao Arroz", 7, datetime(2026, 3, 15, 14, 30))

    response = client.get("/listar-movimentacoes")
    html = response.data.decode()

    assert response.status_code == 200
    assert "Teste Movimentacao Arroz" in html
    assert "Venda" in html
    assert "<td>7</td>" in html
    assert "15/03/2026 14:30" in html
    assert "Nenhuma movimentação" not in html


def test_api_returns_movements_in_order(client):
    _create_movement("Teste Movimentacao Antiga", 1, datetime(2026, 1, 1, 10, 0))
    _create_movement("Teste Movimentacao Recente", 2, datetime(2026, 2, 1, 10, 0))

    response = client.get("/listar-movimentacoes/api")
    data = response.get_json()

    assert response.status_code == 200
    assert [item["product"] for item in data] == [
        "Teste Movimentacao Recente",
        "Teste Movimentacao Antiga",
    ]
    assert data[0]["type_label"] == "Venda"
    assert data[0]["quantity"] == 2
