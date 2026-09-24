from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import Product


def list_promotional_products(session: Session) -> list[Product]:
    statement = select(Product).where(Product.promotional.is_(True)).order_by(Product.name)
    return list(session.scalars(statement))
