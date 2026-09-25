from flask import Blueprint, jsonify, render_template

from app.features.bloquear_quantidade.service import status

bp = Blueprint(
    "bloquear_quantidade",
    __name__,
    url_prefix="/bloquear-quantidade",
    template_folder="templates",
)

@bp.get("")
def page():
    return render_template("bloquear-quantidade.html")


@bp.get("/api")
def api():
    return jsonify(status())
