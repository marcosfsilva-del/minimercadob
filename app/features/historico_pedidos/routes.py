from flask import Blueprint, jsonify, render_template

from app.features.historico_pedidos.service import status

bp = Blueprint(
    "historico_pedidos",
    __name__,
    url_prefix="/historico-pedidos",
    template_folder="templates",
)


@bp.get("")
def page():
    return render_template("historico-pedidos.html")


@bp.get("/api")
def api():
    return jsonify(status())
