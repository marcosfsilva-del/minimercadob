from flask import Blueprint, Response, g, render_template, request, url_for

from app.core.database import session_scope
from app.features.compra_finalizada.service import (
    find_public_code_created_after,
    latest_order_id,
    load_order_summary,
)

CHECKOUT_ENDPOINT = "web.finish_checkout"
REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})

bp = Blueprint(
    "compra_finalizada",
    __name__,
    url_prefix="/compra-finalizada",
    template_folder="templates",
)


@bp.get("/<public_code>")
def page(public_code: str):
    with session_scope() as db:
        order = load_order_summary(db, public_code)

    if order is None:
        return render_template(
            "compra-finalizada.html", order=None, public_code=public_code
        ), 404

    return render_template("compra-finalizada.html", order=order, public_code=public_code)


@bp.before_app_request
def remember_last_order() -> None:
    """Guarda qual era o ultimo pedido antes do checkout do core criar o novo."""
    if request.endpoint != CHECKOUT_ENDPOINT:
        return

    with session_scope() as db:
        g.order_id_before_checkout = latest_order_id(db)


@bp.after_app_request
def redirect_to_success(response: Response) -> Response:
    """Manda o checkout do core para a tela de sucesso, sem alterar `app/core`."""
    if request.endpoint != CHECKOUT_ENDPOINT or response.status_code not in REDIRECT_STATUSES:
        return response

    with session_scope() as db:
        public_code = find_public_code_created_after(db, g.get("order_id_before_checkout"))

    if public_code is None:
        return response

    # Mantem a resposta do core (cookie de sessao, flash) e so troca o destino.
    response.headers["Location"] = url_for("compra_finalizada.page", public_code=public_code)
    return response
