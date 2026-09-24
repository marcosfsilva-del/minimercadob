from flask import Blueprint, jsonify, render_template

from app.features.desconto_por_categoria.service import status

bp = Blueprint("desconto_por_categoria", __name__, url_prefix="/desconto-por-categoria", template_folder="templates")


@bp.get("")
def page():
    return render_template("desconto-por-categoria.html")


@bp.get("/api")
def api():
    return jsonify(status())
