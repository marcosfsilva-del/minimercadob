import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import create_app, database
from app.core.models import Order, Product


@pytest.fixture
def app_with_product(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(
        database,
        "SessionLocal",
        sessionmaker(bind=engine, autoflush=False, expire_on_commit=False),
    )

    app = create_app()
    with database.SessionLocal() as db:
        product = Product(
            name="Arroz",
            description="Arroz branco",
            category="Mercearia",
            price=10.0,
            stock=5,
            promotional=False,
        )
        db.add(product)
        db.commit()
        product_id = product.id

    return app, product_id


def _set_cart(client, product_id):
    with client.session_transaction() as session:
        session["cart"] = {str(product_id): 1}


def test_checkout_offers_pickup_and_delivery(app_with_product):
    app, product_id = app_with_product
    client = app.test_client()
    _set_cart(client, product_id)

    response = client.get("/checkout")

    assert response.status_code == 200
    assert b"Retirada" in response.data
    assert b"Entrega" in response.data
    assert b'name="delivery_method"' in response.data


def test_checkout_pickup_without_address_creates_order(app_with_product):
    app, product_id = app_with_product
    client = app.test_client()
    _set_cart(client, product_id)

    response = client.post("/checkout", data={"delivery_method": "retirada"})

    assert response.status_code == 302

    with database.SessionLocal() as db:
        order = db.query(Order).one()
        assert order.delivery_method == "retirada"
        assert order.delivery_address is None


def test_checkout_delivery_without_address_is_rejected(app_with_product):
    app, product_id = app_with_product
    client = app.test_client()
    _set_cart(client, product_id)

    response = client.post("/checkout", data={"delivery_method": "entrega"})

    assert response.status_code == 400
    assert "Endereço é obrigatório para entrega".encode() in response.data

    with database.SessionLocal() as db:
        assert db.query(Order).count() == 0


def test_checkout_delivery_with_address_creates_order(app_with_product):
    app, product_id = app_with_product
    client = app.test_client()
    _set_cart(client, product_id)

    response = client.post(
        "/checkout",
        data={"delivery_method": "entrega", "delivery_address": "Rua B, 456"},
    )

    assert response.status_code == 302

    with database.SessionLocal() as db:
        order = db.query(Order).one()
        assert order.delivery_method == "entrega"
        assert order.delivery_address == "Rua B, 456"
