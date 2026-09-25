from contextlib import contextmanager

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import create_app
from app.core.database import Base
from app.core.models import Product
from app.features.reposicao_estoque.service import (
    MOVEMENT_TYPE,
    list_replenishment_movements,
    replenish_stock,
)


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    session.add(
        Product(
            name="Arroz",
            description="Pacote de arroz",
            category="Mercearia",
            price=10.0,
            stock=10,
            promotional=False,
        )
    )
    session.commit()
    yield session
    session.close()


def _product(db):
    return db.scalars(select(Product)).one()


def test_reposicao_aumenta_estoque(db):
    product = _product(db)

    replenish_stock(db, product.id, 5)
    db.commit()

    assert product.stock == 15


def test_reposicao_rejeita_quantidade_invalida(db):
    product = _product(db)

    for quantity in (0, -3):
        with pytest.raises(ValueError, match="maior que zero"):
            replenish_stock(db, product.id, quantity)

    assert product.stock == 10
    assert list_replenishment_movements(db) == []


def test_reposicao_registra_movimento(db, monkeypatch):
    product = _product(db)

    @contextmanager
    def fake_scope():
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise

    monkeypatch.setattr("app.features.reposicao_estoque.routes.session_scope", fake_scope)
    client = create_app().test_client()

    page = client.get("/reposicao-estoque")
    assert page.status_code == 200
    assert b'name="product_id"' in page.data
    assert b'name="quantity"' in page.data
    assert "Arroz" in page.get_data(as_text=True)

    response = client.post(
        "/reposicao-estoque",
        data={"product_id": str(product.id), "quantity": "5"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Arroz" in body
    assert "Reposição" in body
    assert "Quantidade: 5" in body
    assert product.stock == 15

    movements = list_replenishment_movements(db)
    assert len(movements) == 1
    assert movements[0].type == MOVEMENT_TYPE
    assert movements[0].product_id == product.id
    assert movements[0].quantity == 5
