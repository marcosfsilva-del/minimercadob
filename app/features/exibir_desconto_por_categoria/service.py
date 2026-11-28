"""Resumo do carrinho com desconto por categoria (requisito 041 - Issue #27).

Usa a regra do requisito 040 (Issue #22) em app/features/desconto_por_categoria.
"""

from app.features.desconto_por_categoria.service import cart_discount, rule


def cart_summary(items: list[dict], total: float) -> dict[str, object]:
    """Monta os valores do resumo: subtotal, desconto e total final."""
    discount = cart_discount(items)
    current_rule = rule()
    return {
        "subtotal": round(total, 2),
        "discount": discount,
        "final_total": round(total - discount, 2),
        "has_discount": discount > 0,
        "category": current_rule["category"],
        "percent": current_rule["percent"],
    }
