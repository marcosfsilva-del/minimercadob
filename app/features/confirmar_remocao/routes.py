from flask import Blueprint, jsonify, render_template

from app.features.confirmar_remocao.service import status

bp = Blueprint(
    "confirmar_remocao",
    __name__,
    url_prefix="/confirmar-remocao",
    template_folder="templates",
)


@bp.get("")
def page():
    return render_template("confirmar-remocao.html")


@bp.get("/api")
def api():
    return jsonify(status())
