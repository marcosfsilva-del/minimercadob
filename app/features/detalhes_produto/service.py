from sqlalchemy.orm import Session

from app.core.models import Product


def get_product(session: Session, product_id: int) -> Product | None:
    """
        Busca o produto pelo id, se nao existir devolve None.
    """
    return session.get(Product, product_id)
