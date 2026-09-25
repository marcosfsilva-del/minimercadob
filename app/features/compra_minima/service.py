
MINIMO_COMPRA = 50.0


def status_checkout(total: float, minimo: float = MINIMO_COMPRA) -> dict[str, object]:
    """
    Decide se o checkout pode ser finalizado com base no total atingir o valor minimo.
    Retorna se pode finalizar e, caso nao atinja, quanto falta.
    """
    pode_finalizar = total >= minimo
    falta = 0.0 if pode_finalizar else round(minimo - total, 2)
    return {
        "total": total,
        "minimo": minimo,
        "pode_finalizar": pode_finalizar,
        "falta": falta,
    }