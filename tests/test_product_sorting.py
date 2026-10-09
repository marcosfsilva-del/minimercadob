import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.models import Product
from app.core.services.market_service import list_products


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(
            [
                Product(
                    name="Banana",
                    description="Fruta",
                    category="Frutas",
                    price=3.0,
                    stock=10,
                ),
                Product(
                    name="Abacaxi",
                    description="Fruta",
                    category="Frutas",
                    price=5.0,
                    stock=10,
                ),
                Product(
                    name="Maçã",
                    description="Fruta",
                    category="Frutas",
                    price=4.0,
                    stock=10,
                ),
            ]
        )
        session.commit()
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.mark.parametrize(
    ("order", "expected"),
    [
        ("asc", ["Abacaxi", "Banana", "Maçã"]),
        ("desc", ["Maçã", "Banana", "Abacaxi"]),
    ],
)
def test_list_products_sorts_by_name(db_session, order, expected):
    products = list_products(db_session, order=order)
    assert [product.name for product in products] == expected
