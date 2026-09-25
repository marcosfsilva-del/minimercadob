from flask import Blueprint, jsonify, render_template

from app.core.database import session_scope
from app.features.listar_movimentacoes.service import list_movements, type_label

bp = Blueprint(
    "listar_movimentacoes",
    __name__,
    url_prefix="/listar-movimentacoes",
    template_folder="templates",
)


@bp.get("")
def page():
    with session_scope() as db:
        movements = list_movements(db)
    return render_template(
        "listar-movimentacoes.html", movements=movements, type_label=type_label
    )


@bp.get("/api")
def api():
    with session_scope() as db:
        movements = list_movements(db)
    return jsonify(
        [
            {
                "id": movement.id,
                "product": movement.product.name,
                "type": movement.type,
                "type_label": type_label(movement.type),
                "quantity": movement.quantity,
                "created_at": movement.created_at.isoformat(),
            }
            for movement in movements
        ]
    )
