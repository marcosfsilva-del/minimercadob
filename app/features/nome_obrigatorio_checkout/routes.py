from flask import Blueprint, jsonify, render_template

from app.features.nome_obrigatorio_checkout.service import status

bp = Blueprint(
    "nome_obrigatorio_checkout",
    __name__,
    url_prefix="/nome-obrigatorio-checkout",
    template_folder="templates",
)


@bp.get("")
def page():
    return render_template("nome-obrigatorio-checkout.html")


@bp.get("/api")
def api():
    return jsonify(status())
