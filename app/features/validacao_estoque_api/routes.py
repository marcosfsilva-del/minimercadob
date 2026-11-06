from flask import Blueprint, jsonify, render_template

from app.features.validacao_estoque_api.service import status

bp = Blueprint("validacao_estoque_api", __name__, url_prefix="/validacao-estoque-api",
                template_folder="templates")


@bp.get("")
def page():
    return render_template("validacao-estoque-api.html")


@bp.get("/api")
def api():
    return jsonify(status())
