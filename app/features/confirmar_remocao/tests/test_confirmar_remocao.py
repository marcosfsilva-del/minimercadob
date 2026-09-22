"""Testes da feature de confirmacao de remocao.

Cada teste abaixo corresponde a um criterio de aceitacao das Issues
#49 (confirmar remocao) e #53 (mensagem apos remover).

A estrutura segue o padrao Dado / Quando / Entao:
  DADO   um estado inicial conhecido
  QUANDO uma acao acontece
  ENTAO  o resultado precisa ser exatamente este
"""

from app.core import create_app
from app.features.confirmar_remocao.service import (
    mensagem_remocao,
    remover_item,
    status,
)

# ---------------------------------------------------------------------------
# TESTES DE UNIDADE - regras puras, sem subir a aplicacao
# ---------------------------------------------------------------------------


def test_remover_item_tira_o_produto_do_carrinho():
    """Criterio #49: confirmar remove o item do carrinho."""
    # DADO um carrinho com dois produtos
    carrinho = {"1": 2, "7": 1}

    # QUANDO removo o produto de id 1
    resultado = remover_item(carrinho, 1)

    # ENTAO ele sai, o outro permanece, e a funcao confirma a remocao
    assert resultado is True
    assert "1" not in carrinho
    assert carrinho == {"7": 1}


def test_remover_item_inexistente_nao_altera_o_carrinho():
    """Criterio #53: cancelar a remocao nao gera mensagem.

    Se nada foi removido, a funcao devolve False - e e esse False que
    impede a mensagem de sucesso de aparecer.
    """
    # DADO um carrinho com um produto
    carrinho = {"7": 1}

    # QUANDO tento remover um produto que nao esta la
    resultado = remover_item(carrinho, 99)

    # ENTAO nada muda e a funcao avisa que nao removeu
    assert resultado is False
    assert carrinho == {"7": 1}


def test_mensagem_remocao_informa_o_nome_do_produto():
    """Criterio #53: a mensagem informa o NOME do produto removido."""
    # DADO o nome de um produto
    # QUANDO monto a mensagem
    mensagem = mensagem_remocao("Café Torrado 500g")

    # ENTAO o nome aparece na mensagem
    assert "Café Torrado 500g" in mensagem
    assert mensagem == "Produto removido do carrinho: Café Torrado 500g."


def test_status_da_feature():
    """Endpoint de diagnostico continua respondendo."""
    assert status() == {"feature": "confirmar-remocao", "status": "ok"}


# ---------------------------------------------------------------------------
# TESTES DE INTEGRACAO - sobem a aplicacao e exercitam as rotas
# ---------------------------------------------------------------------------


def _cliente_com_produto_no_carrinho():
    """Prepara um cliente de teste com um produto real no carrinho.

    Devolve o cliente e o produto usado, para os testes poderem conferir
    o nome que deve aparecer na mensagem.
    """
    from app.core.database import session_scope
    from app.core.services.market_service import list_products

    app = create_app()
    client = app.test_client()

    with app.app_context():
        with session_scope() as db:
            produto = list_products(db)[0]
            produto_id = produto.id
            produto_nome = produto.name

    # Adiciona o produto ao carrinho usando a rota do proprio core.
    client.post(f"/cart/add/{produto_id}")

    return client, produto_id, produto_nome


def test_pagina_de_confirmacao_pergunta_antes_de_remover():
    """Criterio #49: clicar em Remover exibe um pedido de confirmacao."""
    # DADO um carrinho com um produto
    client, produto_id, produto_nome = _cliente_com_produto_no_carrinho()

    # QUANDO abro a pagina de confirmacao
    resposta = client.get(f"/confirmar-remocao/{produto_id}")

    # ENTAO a pagina pergunta, mostrando o nome do produto
    assert resposta.status_code == 200
    assert "Confirmar remoção".encode() in resposta.data
    assert produto_nome.encode() in resposta.data


def test_cancelar_mantem_o_item_no_carrinho():
    """Criterio #49: cancelar mantem o item, com a mesma quantidade."""
    # DADO um carrinho com um produto
    client, produto_id, _ = _cliente_com_produto_no_carrinho()

    # QUANDO apenas VISITO a pagina de confirmacao e volto ao carrinho
    # (e exatamente o que o botao Cancelar faz: nao envia POST)
    client.get(f"/confirmar-remocao/{produto_id}")

    # ENTAO o produto continua no carrinho
    with client.session_transaction() as sessao:
        assert sessao["cart"] == {str(produto_id): 1}


def test_confirmar_remove_o_item_e_exibe_mensagem_com_o_nome():
    """Criterios #49 e #53: confirmar remove o item e informa o produto."""
    # DADO um carrinho com um produto
    client, produto_id, produto_nome = _cliente_com_produto_no_carrinho()

    # QUANDO envio o POST de confirmacao e sigo o redirecionamento
    resposta = client.post(
        f"/confirmar-remocao/{produto_id}",
        follow_redirects=True,
    )

    # ENTAO o carrinho fica vazio
    with client.session_transaction() as sessao:
        assert sessao["cart"] == {}

    # E a mensagem exibida traz o nome do produto removido
    assert resposta.status_code == 200
    assert produto_nome.encode() in resposta.data
    assert b"Produto removido do carrinho" in resposta.data


def test_mensagem_aparece_apenas_uma_vez():
    """Criterio #53: a mensagem aparece apenas uma vez.

    O flash do Flask e consumido na primeira leitura. Recarregar a pagina
    nao pode repetir a mensagem.
    """
    # DADO um produto removido com confirmacao
    client, produto_id, _ = _cliente_com_produto_no_carrinho()
    client.post(f"/confirmar-remocao/{produto_id}", follow_redirects=True)

    # QUANDO recarrego o carrinho
    segunda_visita = client.get("/cart")

    # ENTAO a mensagem nao aparece de novo
    assert b"Produto removido do carrinho" not in segunda_visita.data