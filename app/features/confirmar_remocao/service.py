"""Regras de negocio da feature de confirmacao de remocao.

As funcoes deste modulo sao PURAS: recebem dados, devolvem dados e nao
dependem do Flask, do banco nem da sessao HTTP. E por isso que elas podem
ser testadas isoladamente, sem subir a aplicacao inteira.
"""


def remover_item(carrinho: dict[str, int], product_id: int) -> bool:
    """Remove um produto do carrinho.

    O carrinho e um dicionario no formato {"id_do_produto": quantidade},
    igual ao que o core guarda na sessao do usuario.

    Devolve True se o item existia e foi removido, e False se ele nem
    estava la. Esse retorno e o que permite decidir se a mensagem de
    sucesso deve ou nao ser exibida.
    """
    return carrinho.pop(str(product_id), None) is not None


def mensagem_remocao(nome_produto: str) -> str:
    """Monta a mensagem exibida apos a remocao.

    O criterio de aceitacao da Issue #53 exige que a mensagem identifique
    o produto PELO NOME, e nao pelo id.
    """
    return f"Produto removido do carrinho: {nome_produto}."


def status() -> dict[str, str]:
    """Endpoint de diagnostico gerado pelo esqueleto da feature."""
    return {"feature": "confirmar-remocao", "status": "ok"}