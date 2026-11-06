from app.core.models import Product

OUT_OF_STOCK_LABEL = "Esgotado"


def is_out_of_stock(product: Product) -> bool:
    """Retorna True quando o estoque do produto é zero (ou negativo)."""
    return product.stock <= 0
