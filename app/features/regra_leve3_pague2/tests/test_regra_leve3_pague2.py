from types import SimpleNamespace

from app.core import create_app
from app.features.regra_leve3_pague2.service import (
    CATEGORIA_PROMOCIONAL,
    calcular_promocao,
    desconto_do_item,
    grupos_promocionais,
    status,
)

PRECO = 2.49


def sabonete():
    return SimpleNamespace(name="Sabonete", category=CATEGORIA_PROMOCIONAL, price=PRECO)


def arroz():
    return SimpleNamespace(name="Arroz", category="Mercearia", price=24.90)


def carrinho(produto, quantidade):
    return [{"product": produto, "quantity": quantidade}]


def test_status():
    assert status() == {"feature": "regra-leve3-pague2", "status": "ok"}


def test_dois_itens_nao_recebem_desconto():
    promocao = calcular_promocao(carrinho(sabonete(), 2))

    assert grupos_promocionais(2) == 0
    assert promocao["economia"] == 0
    assert promocao["aplicou"] is False
    assert promocao["total_final"] == round(PRECO * 2, 2)


def test_tres_itens_recebem_um_desconto():
    promocao = calcular_promocao(carrinho(sabonete(), 3))

    assert grupos_promocionais(3) == 1
    assert promocao["economia"] == PRECO
    assert promocao["aplicou"] is True
    assert promocao["total_final"] == round(PRECO * 2, 2)


def test_seis_itens_recebem_dois_descontos():
    promocao = calcular_promocao(carrinho(sabonete(), 6))

    assert grupos_promocionais(6) == 2
    assert promocao["economia"] == round(PRECO * 2, 2)
    assert promocao["total_final"] == round(PRECO * 4, 2)
    assert promocao["itens_com_desconto"][0]["unidades_gratuitas"] == 2


def test_quatro_itens_recebem_apenas_um_desconto():
    assert desconto_do_item(PRECO, 4) == PRECO


def test_produto_de_outra_categoria_nao_recebe_desconto():
    promocao = calcular_promocao(carrinho(arroz(), 6))

    assert promocao["economia"] == 0
    assert promocao["aplicou"] is False





def test_pagina_da_feature_documenta_a_categoria():
    app = create_app()
    client = app.test_client()

    response = client.get("/regra-leve3-pague2")

    assert response.status_code == 200
    assert CATEGORIA_PROMOCIONAL.encode() in response.data


def test_api_da_feature_publica_a_regra():
    app = create_app()
    client = app.test_client()

    payload = client.get("/regra-leve3-pague2/api").get_json()

    assert payload["categoria"] == CATEGORIA_PROMOCIONAL
    assert payload["regra"] == "Leve 3, pague 2"
