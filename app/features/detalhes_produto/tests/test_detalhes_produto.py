import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from app.core import create_app
from app.core.database import Base, init_database, session_scope
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


@pytest.fixture
def product():
    """Produto criado no banco da aplicacao para os testes de rota e removido ao final."""
    init_database()
    with session_scope() as session:
        created = Product(
            name="Feijao de teste",
            description="Pacote de feijao carioca 1kg",
            category="Mercearia",
            price=8.49,
            stock=12,
        )
        session.add(created)
    yield created
    with session_scope() as session:
        session.execute(delete(Product).where(Product.id == created.id))


def test_get_product_devolve_produto_existente(db):
    product = get_product(db, 1)

    assert product is not None
    assert product.name == "Arroz"
    assert product.category == "Mercearia"


def test_get_product_devolve_none_para_id_inexistente(db):
    assert get_product(db, 9999) is None


def test_pagina_exibe_todos_os_campos_do_produto(product):
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


def test_catalogo_exibe_link_para_os_detalhes(product):
    response = create_app().test_client().get("/")

    assert f'href="/produto/{product.id}"' in response.data.decode()


# Adicionar ao carrinho pela pagina de detalhes


def test_pagina_de_detalhes_possui_botao_de_adicionar(product):
    response = create_app().test_client().get(f"/produto/{product.id}")
    body = response.data.decode()

    assert f'action="/produto/{product.id}/adicionar"' in body
    assert "Adicionar ao carrinho" in body


def test_botao_adiciona_o_produto_correto():
    client = create_app().test_client()
    with session_scope() as session:
        outro = Product(name="Outro", description="x", category="x", price=1.0, stock=5)
        alvo = Product(name="Alvo", description="x", category="x", price=2.0, stock=5)
        session.add_all([outro, alvo])
    try:
        client.post(f"/produto/{alvo.id}/adicionar")
        client.post(f"/produto/{alvo.id}/adicionar")

        with client.session_transaction() as flask_session:
            assert flask_session["cart"] == {str(alvo.id): 2}
    finally:
        with session_scope() as session:
            session.execute(delete(Product).where(Product.id.in_([outro.id, alvo.id])))


def test_adicionar_volta_para_os_detalhes_sem_erro(product):
    client = create_app().test_client()

    response = client.post(f"/produto/{product.id}/adicionar", follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == f"/produto/{product.id}"
    assert "adicionado ao carrinho" in response.data.decode()


def test_adicionar_e_seguir_para_o_carrinho_sem_erro(product):
    client = create_app().test_client()

    response = client.post(
        f"/produto/{product.id}/adicionar",
        data={"destino": "carrinho"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.request.path == "/cart"
    assert product.name in response.data.decode()


def test_adicionar_produto_inexistente_retorna_404_e_nao_altera_carrinho():
    client = create_app().test_client()

    response = client.post("/produto/999999/adicionar")

    assert response.status_code == 404
    with client.session_transaction() as flask_session:
        assert flask_session.get("cart", {}) == {}
