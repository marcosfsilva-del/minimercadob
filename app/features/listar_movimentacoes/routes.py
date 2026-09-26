from flask import Blueprint, jsonify, render_template

from app.features.listar_movimentacoes.service import status

bp = Blueprint(
    "listar_movimentacoes", 
    __name__, 
    url_prefix="/listar-movimentacoes", 
    template_folder="templates"
)


@bp.get("")
def page():
    return render_template("listar-movimentacoes.html")


@bp.get("/api")
def api():
    return jsonify(status())