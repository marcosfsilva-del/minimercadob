from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import Product

MAX_RECENTLY_VIEWED = 10


def register_recently_viewed(
    recently_viewed: list[int],
    product_id: int,
    limit: int = MAX_RECENTLY_VIEWED,
) -> list[int]:
    
    if limit < 1:
        raise ValueError("limit deve ser maior que zero.")

    without_duplicate = [pid for pid in recently_viewed if pid != product_id]
    updated = [product_id, *without_duplicate]
    return updated[:limit]


def get_product(session: Session, product_id: int) -> Product | None:
    return session.get(Product, product_id)


def get_products_by_ids(session: Session, product_ids: list[int]) -> list[Product]:
   
    if not product_ids:
        return []

    products = session.scalars(select(Product).where(Product.id.in_(product_ids))).all()
    product_by_id = {product.id: product for product in products}
    return [product_by_id[pid] for pid in product_ids if pid in product_by_id]