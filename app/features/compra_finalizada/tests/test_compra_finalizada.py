import os
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.core.database as database_module
from app.core.database import session_scope
from app.core.models import Order, Product


@pytest.fixture()
def client(monkeypatch):
    """App apontando para um SQLite temporario, isolado do banco de desenvolvimento."""
    database_path = os.path.join(tempfile.mkdtemp(), "compra_finalizada.db")
    engine = create_engine(f"sqlite:///{database_path}", future=True)

    monkeypatch.setattr(database_module, "engine", engine)
    monkeypatch.setattr(
        database_module,
        "SessionLocal",
        sessionmaker(bind=engine, autoflush=False, expire_on_commit=False),
    )

    from app.core import create_app

    application = create_app()
    application.config.update(TESTING=True)
    return application.test_client()


@pytest.fixture()
def product(client):
    with session_scope() as db:
        item = Product(
            name="Arroz 5kg",
            description="Tipo 1",
            category="Mercearia",
            price=24.90,
            stock=10,
            promotional=False,
        )
        db.add(item)
        db.flush()
        return item.id


def _finish_purchase(client, product_id, quantity=2, customer_name="Gustavo"):
    client.post(f"/cart/add/{product_id}")
    client.post(f"/cart/update/{product_id}", data={"quantity": str(quantity)})
    return client.post("/checkout", data={"customer_name": customer_name})


def test_checkout_redireciona_para_a_tela_de_sucesso(client, product):
    response = _finish_purchase(client, product)

    with session_scope() as db:
        public_code = db.query(Order).one().public_code

    assert response.status_code == 302
    assert response.headers["Location"] == f"/compra-finalizada/{public_code}"


def test_tela_mostra_codigo_do_pedido_e_total_da_compra(client, product):
    redirect = _finish_purchase(client, product, quantity=2)

    with session_scope() as db:
        public_code = db.query(Order).one().public_code

    response = client.get(redirect.headers["Location"])
    body = response.data.decode()

    assert response.status_code == 200
    assert public_code in body
    assert "R$ 49,80" in body
    assert "2x Arroz 5kg" in body
    assert "Gustavo" in body


def test_tela_tem_acoes_para_catalogo_e_pedidos(client, product):
    redirect = _finish_purchase(client, product)

    body = client.get(redirect.headers["Location"]).data.decode()

    assert 'href="/"' in body
    assert 'href="/orders"' in body


def test_codigo_inexistente_mostra_mensagem_amigavel(client):
    response = client.get("/compra-finalizada/ZZZ-9999")

    assert response.status_code == 404
    assert "Pedido não encontrado" in response.data.decode()


def test_demais_rotas_nao_sao_redirecionadas_pelo_hook(client, product):
    assert client.get("/").status_code == 200
    assert client.post(f"/cart/add/{product}").headers["Location"] == "/"
