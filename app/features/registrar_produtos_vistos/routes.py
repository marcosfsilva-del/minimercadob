from flask import Blueprint, abort, render_template, session

from app.core.database import session_scope
from app.features.recently_viewed.service import (
    get_product,
    get_products_by_ids,
    register_recently_viewed,
)

recently_viewed_bp = Blueprint(
    "recently_viewed",
    __name__,
    template_folder="templates",
)

SESSION_KEY = "recently_viewed"


def _recently_viewed_ids() -> list[int]:
    return session.setdefault(SESSION_KEY, [])


@recently_viewed_bp.get("/produtos/<int:product_id>")
def product_detail(product_id: int):
    with session_scope() as db:
        product = get_product(db, product_id)
        if product is None:
            abort(404)

        updated_ids = register_recently_viewed(_recently_viewed_ids(), product_id)
        session[SESSION_KEY] = updated_ids
        session.modified = True

        other_ids = [pid for pid in updated_ids if pid != product_id]
        recently_viewed_products = get_products_by_ids(db, other_ids)

    return render_template(
        "product_detail.html",
        product=product,
        recently_viewed=recently_viewed_products,
    )