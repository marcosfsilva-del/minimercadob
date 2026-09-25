from flask import Blueprint, jsonify, render_template, request

from app.core.database import session_scope
from app.core.services.market_service import order_to_dict
from app.features.historico_pedidos.service import buscar_historico

bp = Blueprint(
    "historico_pedidos",
    __name__,
    url_prefix="/historico-pedidos",
    template_folder="templates",
)


@bp.get("")
def page():
    termo = request.args.get("cliente", "").strip()
    with session_scope() as db:
        pedidos = buscar_historico(db, termo)
        return render_template("historico-pedidos.html", pedidos=pedidos, termo=termo)


@bp.get("/api")
def api():
    termo = request.args.get("cliente", "").strip()
    with session_scope() as db:
        pedidos = buscar_historico(db, termo)
        return jsonify([order_to_dict(pedido) for pedido in pedidos])
