from contextlib import contextmanager

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core import create_app
from app.core.database import Base
from app.core.models import Customer, InventoryMovement, Order, Product
from app.core.routes import web
from app.features.cpf_checkout import routes
from app.features.cpf_checkout.service import validar_cpf


@pytest.mark.parametrize("cpf", ["12345678901", "123.456.789-01"])
def test_aceita_cpf_com_e_sem_pontuacao(cpf):
    assert validar_cpf(cpf) == "12345678901"


@pytest.mark.parametrize("cpf", ["", "123", "123456789012", "abcdefghijk", "1234567890a",
                                 "123.456789-01", "１２３４５６７８９０１"])
def test_rejeita_cpf_invalido(cpf):
    with pytest.raises(ValueError, match="11 dígitos"):
        validar_cpf(cpf)


@pytest.fixture
def checkout(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'teste.db'}")
    Base.metadata.create_all(engine)

    @contextmanager
    def banco_teste():
        with Session(engine, expire_on_commit=False) as db, db.begin():
            yield db

    monkeypatch.setattr(web, "session_scope", banco_teste)
    monkeypatch.setattr(routes, "session_scope", banco_teste)
    with banco_teste() as db:
        db.add(Product(id=1, name="arroz", description="pacote", category="alimentos",
                       price=10, stock=5))
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    with client.session_transaction() as sessao:
        sessao["cart"] = {"1": 2}
    yield client, banco_teste
    engine.dispose()


def test_campo_aparece_no_checkout(checkout):
    client, _ = checkout
    resposta = client.get("/checkout")
    assert resposta.status_code == 200
    assert b'for="cpf"' in resposta.data
    assert b'name="cpf"' in resposta.data


@pytest.mark.parametrize("cpf", ["12345678901", "123.456.789-01"])
def test_checkout_persiste_cpf_e_pedido(checkout, cpf):
    client, banco_teste = checkout
    resposta = client.post("/checkout", data={"customer_name": "ana", "cpf": cpf})
    assert resposta.status_code == 302
    assert resposta.location.endswith("/orders")
    with banco_teste() as db:
        cliente = db.scalar(select(Customer))
        assert cliente.name == "ana"
        assert cliente.cpf == "12345678901"
        pedido = db.scalar(select(Order))
        assert pedido.customer_name == "ana"
        assert pedido.total == 20
        assert db.get(Product, 1).stock == 3
    with client.session_transaction() as sessao:
        assert sessao["cart"] == {}


@pytest.mark.parametrize("dados", [{}, {"cpf": "123"}, {"cpf": "abcdefghijk"}])
def test_cpf_invalido_preserva_carrinho_e_banco(checkout, dados):
    client, banco_teste = checkout
    resposta = client.post("/checkout", data=dados)
    assert resposta.status_code == 400
    assert "informe um cpf com 11 dígitos".encode() in resposta.data
    with banco_teste() as db:
        assert db.scalar(select(Order)) is None
        assert db.scalar(select(Customer)) is None
        assert db.scalar(select(InventoryMovement)) is None
        assert db.get(Product, 1).stock == 5
    with client.session_transaction() as sessao:
        assert sessao["cart"] == {"1": 2}


def test_falta_de_estoque_nao_salva_cliente(checkout):
    client, banco_teste = checkout
    with client.session_transaction() as sessao:
        sessao["cart"] = {"1": 6}
    resposta = client.post("/checkout", data={"cpf": "12345678901"})
    assert resposta.status_code == 400
    with banco_teste() as db:
        assert db.scalar(select(Customer)) is None
        assert db.scalar(select(Order)) is None
        assert db.get(Product, 1).stock == 5
