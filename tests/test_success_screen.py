"""Testes da tela de sucesso exibida depois de finalizar a compra.

Cobre os criterios de aceitacao da issue:

1. usuario e redirecionado apos a compra;
2. a tela mostra o codigo do pedido;
3. a tela mostra o total da compra.
"""

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
    database_path = os.path.join(tempfile.mkdtemp(), "success_screen.db")
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
def catalogo(client):
    """Dois produtos, para o total nao ser apenas o preco de um item."""
    with session_scope() as db:
        cafe = Product(
            name="Café",
            description="Torrado e moído 500g",
            category="Bebidas",
            price=15.90,
            stock=20,
            promotional=False,
        )
        leite = Product(
            name="Leite",
            description="Integral 1L",
            category="Laticínios",
            price=4.79,
            stock=30,
            promotional=False,
        )
        db.add_all([cafe, leite])
        db.flush()
        return {"cafe": cafe.id, "leite": leite.id}


def _finalizar_compra(client, catalogo):
    """Percorre o fluxo real do site: 1x Café + 3x Leite = R$ 30,27."""
    client.post(f"/cart/add/{catalogo['cafe']}")
    client.post(f"/cart/add/{catalogo['leite']}")
    client.post(f"/cart/update/{catalogo['leite']}", data={"quantity": "3"})
    return client.post("/checkout", data={"customer_name": "Gustavo Cirino"})


def _pedido_criado() -> tuple[str, float]:
    """Codigo publico e total do unico pedido do banco de teste."""
    with session_scope() as db:
        order = db.query(Order).one()
        return order.public_code, order.total


def _abrir_tela(client, resposta_do_checkout):
    return client.get(resposta_do_checkout.headers["Location"])


def test_usuario_e_redirecionado_para_a_tela_de_sucesso(client, catalogo):
    resposta = _finalizar_compra(client, catalogo)

    public_code, _ = _pedido_criado()

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == f"/compra-finalizada/{public_code}"


def test_tela_mostra_o_codigo_do_pedido(client, catalogo):
    resposta = _finalizar_compra(client, catalogo)
    public_code, _ = _pedido_criado()

    pagina = _abrir_tela(client, resposta)
    corpo = pagina.data.decode()

    assert pagina.status_code == 200
    assert "Código do pedido" in corpo
    assert public_code in corpo


def test_tela_mostra_o_total_da_compra(client, catalogo):
    resposta = _finalizar_compra(client, catalogo)
    _, total = _pedido_criado()

    corpo = _abrir_tela(client, resposta).data.decode()

    assert total == pytest.approx(30.27)
    assert "Total da compra" in corpo
    assert "R$ 30,27" in corpo
