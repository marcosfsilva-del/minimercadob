import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core import create_app
from app.core.database import Base, session_scope
from app.core.models import Product
from app.features.detalhes_produto.service import get_product


@pytest.fixture
def db():
    """Banco em memoria, criado e destruido a cada teste."""
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(
            Product(
                id=1,
                name="Arroz",
                description="Pacote de arroz branco 5kg",
                category="Mercearia",
                price=24.90,
                stock=30,
            )
        )
        session.commit()
        yield session


def primeiro_produto():
    """Produto real do banco da aplicacao, usado nos testes de rota."""
    with session_scope() as session:
        return session.scalars(select(Product).order_by(Product.id)).first()


def test_get_product_devolve_produto_existente(db):
    product = get_product(db, 1)

    assert product is not None
    assert product.name == "Arroz"
    assert product.category == "Mercearia"


def test_get_product_devolve_none_para_id_inexistente(db):
    assert get_product(db, 9999) is None


def test_pagina_exibe_todos_os_campos_do_produto():
    product = primeiro_produto()
    assert product is not None, "Banco vazio. Rode: python3 tasks.py db-seed"

    response = create_app().test_client().get(f"/produto/{product.id}")
    body = response.data.decode()

    assert response.status_code == 200
    assert product.name in body
    assert product.description in body
    assert product.category in body
    assert str(product.stock) in body


def test_pagina_de_produto_inexistente_retorna_404():
    response = create_app().test_client().get("/produto/999999")

    assert response.status_code == 404
    assert "não encontrado" in response.data.decode()


def test_catalogo_exibe_link_para_os_detalhes():
    product = primeiro_produto()
    assert product is not None, "Banco vazio. Rode: python3 tasks.py db-seed"

    response = create_app().test_client().get("/")

    assert f'href="/produto/{product.id}"' in response.data.decode()
