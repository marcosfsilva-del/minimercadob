"""Regra de promocao "Leve 3, Pague 2" do DevOps Market.

A regra vale para a categoria documentada em CATEGORIA_PROMOCIONAL: a cada
grupo de 3 unidades do mesmo produto dessa categoria, 1 unidade sai de graca.
Quantidades menores que 3 nao recebem desconto.
"""

LEVAR = 3
PAGAR = 2
CATEGORIA_PROMOCIONAL = "Higiene"


def status() -> dict[str, str]:
    return {"feature": "regra-leve3-pague2", "status": "ok"}


def produto_elegivel(produto) -> bool:
    """Diz se o produto participa da promocao (regra por categoria)."""
    return getattr(produto, "category", None) == CATEGORIA_PROMOCIONAL


def grupos_promocionais(quantidade: int) -> int:
    """Quantos grupos completos de 3 existem na quantidade informada."""
    if quantidade < LEVAR:
        return 0
    return quantidade // LEVAR


def unidades_gratuitas(quantidade: int) -> int:
    """Unidades que saem de graca: 1 por grupo completo de 3."""
    return grupos_promocionais(quantidade) * (LEVAR - PAGAR)


def desconto_do_item(preco_unitario: float, quantidade: int) -> float:
    """Valor economizado em um item, ja arredondado para centavos."""
    return round(preco_unitario * unidades_gratuitas(quantidade), 2)


def calcular_promocao(itens) -> dict[str, object]:
    """Aplica a regra sobre os itens do carrinho.

    Cada item deve ter as chaves ``product`` (com ``category``, ``price`` e
    ``name``) e ``quantity``. Devolve o total sem desconto, a economia, o
    total final e a lista de itens que receberam desconto.
    """
    total_sem_desconto = 0.0
    economia = 0.0
    itens_com_desconto: list[dict[str, object]] = []

    for item in itens:
        produto = item["product"]
        quantidade = int(item["quantity"])
        total_sem_desconto += produto.price * quantidade

        if not produto_elegivel(produto):
            continue

        desconto = desconto_do_item(produto.price, quantidade)
        if desconto <= 0:
            continue

        economia += desconto
        itens_com_desconto.append(
            {
                "produto": produto.name,
                "quantidade": quantidade,
                "grupos": grupos_promocionais(quantidade),
                "unidades_gratuitas": unidades_gratuitas(quantidade),
                "desconto": desconto,
            }
        )

    total_sem_desconto = round(total_sem_desconto, 2)
    economia = round(economia, 2)

    return {
        "categoria": CATEGORIA_PROMOCIONAL,
        "regra": f"Leve {LEVAR}, pague {PAGAR}",
        "total_sem_desconto": total_sem_desconto,
        "economia": economia,
        "total_final": round(total_sem_desconto - economia, 2),
        "aplicou": economia > 0,
        "itens_com_desconto": itens_com_desconto,
    }
