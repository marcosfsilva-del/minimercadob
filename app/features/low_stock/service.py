from typing import Any

# Limite documentado para estoque baixo (Requisito 016)
LOW_STOCK_THRESHOLD = 5


def is_low_stock(product: Any) -> bool:
    """Verifica se o produto está com estoque baixo (menor ou igual a 5)."""
    if product is None:
        return False
    stock = getattr(product, "stock", None)
    return stock is not None and stock <= LOW_STOCK_THRESHOLD


def filter_low_stock(products: list[Any]) -> list[Any]:
    """Filtra e retorna apenas produtos com estoque baixo."""
    return [p for p in products if is_low_stock(p)]


def render_product_card_warning(product: Any = None, **_kwargs: Any) -> str:
    """Renderizador injetado no slot PRODUCT_CARD para exibir o alerta visual."""
    if is_low_stock(product):
        return (
            '<div style="background-color: #fef08a; color: #854d0e; padding: 4px 8px; '
            'border-radius: 4px; font-size: 12px; font-weight: bold; margin-bottom: 8px;">'
            f'⚠️ Estoque Baixo ({product.stock} un.)</div>'
        )
    return ""


def render_toolbar_button(**_kwargs: Any) -> str:
    """Renderizador injetado no slot PRODUCT_LIST_TOOLBAR para filtrar no catálogo."""
    return (
        '<a href="/low-stock" class="button-link" style="font-size: 13px;">'
        '⚠️ Ver Estoque Baixo</a>'
    )