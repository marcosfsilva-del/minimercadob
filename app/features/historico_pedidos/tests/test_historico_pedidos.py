"""Testes do Módulo 24, histórico de pedidos.

Cobrem os critérios de aceitação dos requisitos 070 e 071:
filtro por cliente, ordenação por data, ordenação por total e as duas juntas.
"""

from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core import create_app
from app.core.database import Base
from app.core.models import Order
from app.features.historico_pedidos import routes
from app.features.historico_pedidos.service import (
    ORDENACAO_PADRAO,
    buscar_historico,
    filtrar_por_cliente,
    ordenacao_valida,
    ordenar_pedidos,
    status,
)


def pedido(numero: int, cliente: str | None, total: float, dia: int) -> Order:
    return Order(
        id=numero,
        customer_name=cliente,
        total=total,
        created_at=datetime(2026, 9, dia, 10, 0),
    )


@pytest.fixture
def pedidos() -> list[Order]:
    return [
        pedido(1, "Ana Souza", 50.0, 10),
        pedido(2, "Bruno Lima", 20.0, 12),
        pedido(3, "ana paula", 80.0, 11),
        pedido(4, None, 35.0, 13),
    ]


def numeros(lista: list[Order]) -> list[int]:
    return [item.id for item in lista]


def test_status():
    assert status() == {"feature": "historico-pedidos", "status": "ok"}


# ------------------------------------------------------------------ filtro, requisito 070


def test_filtro_encontra_pedidos_pelo_nome_do_cliente(pedidos):
    assert numeros(filtrar_por_cliente(pedidos, "Bruno")) == [2]


def test_filtro_aceita_parte_do_nome(pedidos):
    assert numeros(filtrar_por_cliente(pedidos, "sou")) == [1]


def test_filtro_nao_diferencia_maiusculas_e_minusculas(pedidos):
    assert numeros(filtrar_por_cliente(pedidos, "ANA")) == [1, 3]
    assert numeros(filtrar_por_cliente(pedidos, "ana")) == [1, 3]


@pytest.mark.parametrize("termo", [None, "", "   "])
def test_sem_termo_mostra_todos_os_pedidos(pedidos, termo):
    assert numeros(filtrar_por_cliente(pedidos, termo)) == [1, 2, 3, 4]


def test_filtro_sem_resultado_devolve_lista_vazia(pedidos):
    assert filtrar_por_cliente(pedidos, "Carlos") == []


def test_pedido_sem_nome_so_aparece_quando_nao_ha_filtro(pedidos):
    assert 4 not in numeros(filtrar_por_cliente(pedidos, "a"))
    assert 4 in numeros(filtrar_por_cliente(pedidos, ""))


# ------------------------------------------------------------------ ordenação, requisito 071


def test_ordena_por_data_mais_recente_primeiro(pedidos):
    assert numeros(ordenar_pedidos(pedidos, "data_desc")) == [4, 2, 3, 1]


def test_ordena_por_data_mais_antiga_primeiro(pedidos):
    assert numeros(ordenar_pedidos(pedidos, "data_asc")) == [1, 3, 2, 4]


def test_ordena_por_maior_total(pedidos):
    assert numeros(ordenar_pedidos(pedidos, "total_desc")) == [3, 1, 4, 2]


def test_ordena_por_menor_total(pedidos):
    assert numeros(ordenar_pedidos(pedidos, "total_asc")) == [2, 4, 1, 3]


@pytest.mark.parametrize("ordem", [None, "", "preco", "DATA_DESC"])
def test_ordenacao_desconhecida_usa_a_padrao(pedidos, ordem):
    assert ordenacao_valida(ordem) == ORDENACAO_PADRAO
    assert ordenar_pedidos(pedidos, ordem) == ordenar_pedidos(pedidos, ORDENACAO_PADRAO)


def test_empate_no_total_e_desempatado_pelo_numero_do_pedido():
    empatados = [pedido(7, "X", 10.0, 1), pedido(5, "Y", 10.0, 2), pedido(6, "Z", 10.0, 3)]
    assert numeros(ordenar_pedidos(empatados, "total_asc")) == [5, 6, 7]


def test_ordenacao_funciona_com_filtro_aplicado(pedidos):
    filtrados = filtrar_por_cliente(pedidos, "ana")

    assert numeros(ordenar_pedidos(filtrados, "total_desc")) == [3, 1]
    assert numeros(ordenar_pedidos(filtrados, "data_asc")) == [1, 3]


# ------------------------------------------------------------------ banco de dados


def test_buscar_historico_filtra_e_ordena_pedidos_do_banco(pedidos):
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(pedidos)
        session.commit()

        resultado = buscar_historico(session, termo="ANA", ordem="total_asc")

    assert numeros(resultado) == [1, 3]


# ------------------------------------------------------------------ página e API


@pytest.fixture
def cliente_http(monkeypatch, pedidos):
    chamadas = []

    def falso_buscar_historico(_session, termo, ordem):
        chamadas.append((termo, ordem))
        return ordenar_pedidos(filtrar_por_cliente(pedidos, termo), ordem)

    monkeypatch.setattr(routes, "buscar_historico", falso_buscar_historico)
    return create_app().test_client(), chamadas


def test_pagina_repassa_filtro_e_ordenacao(cliente_http):
    client, chamadas = cliente_http

    resposta = client.get("/historico-pedidos?cliente=%20ana%20&ordem=total_desc")

    assert resposta.status_code == 200
    assert chamadas == [("ana", "total_desc")]
    corpo = resposta.data.decode()
    assert corpo.index("Pedido #3") < corpo.index("Pedido #1")
    assert "Pedido #2" not in corpo
    assert 'value="total_desc" selected' in corpo


def test_pagina_sem_resultado_mostra_aviso(cliente_http):
    client, _ = cliente_http

    resposta = client.get("/historico-pedidos?cliente=Carlos")

    assert "Nenhum pedido encontrado para este cliente." in resposta.data.decode()


def test_api_devolve_pedidos_filtrados_e_ordenados(cliente_http):
    client, _ = cliente_http

    resposta = client.get("/historico-pedidos/api?cliente=ana&ordem=data_asc")

    assert resposta.status_code == 200
    assert [item["id"] for item in resposta.get_json()] == [1, 3]
