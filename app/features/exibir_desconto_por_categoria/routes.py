from flask import Blueprint, jsonify, render_template

from app.features.exibir_desconto_por_categoria.service import status

bp = Blueprint("exibir_desconto_por_categoria", __name__, url_prefix="/exibir-desconto-por-categoria", template_folder="templates")


@bp.get("")
def page():
    return render_template("exibir-desconto-por-categoria.html")


@bp.get("/api")
def api():
    return jsonify(status())
