def status():
    return {"feature": "bloquear_quantidade", "status": "active"}


def validar_quantidade_estoque(quantidade: int, estoque: int) -> bool:
    """
    Verifica se a quantidade solicitada ultrapassa o estoque disponivel.
    Retorna False se a quantidade for maior que o estoque (bloqueio #116).
    """
    if quantidade > estoque:
        return False
    return True