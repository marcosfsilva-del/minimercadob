"""Regra de desconto por categoria (requisito 040 - Issue #22)."""

DISCOUNT_CATEGORY = "Mercearia"
DISCOUNT_PERCENT = 10


def has_discount(category: str) -> bool:
    """Retorna True somente para a categoria definida na regra."""
    return category.strip().lower() == DISCOUNT_CATEGORY.lower()


def discounted_price(price: float, category: str) -> float:
    """Preço final do produto: com desconto na categoria definida, igual nas demais."""
    if not has_discount(category):
        return price
    return round(price * (1 - DISCOUNT_PERCENT / 100), 2)


def cart_discount(items: list[dict]) -> float:
    """Soma do desconto de um carrinho.

    Cada item segue o formato do carrinho do core: {"product": Product, "quantity": int}.
    """
    total = 0.0
    for item in items:
        product = item["product"]
        unit_discount = product.price - discounted_price(product.price, product.category)
        total += unit_discount * item["quantity"]
    return round(total, 2)


def rule() -> dict[str, object]:
    return {"category": DISCOUNT_CATEGORY, "percent": DISCOUNT_PERCENT}
