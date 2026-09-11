from flask import Blueprint, jsonify, render_template

from app.features.regra_leve3_pague2.service import status

bp = Blueprint(
    "regra_leve3_pague2",
    __name__,
    url_prefix="/regra-leve3-pague2",
    template_folder="templates",
)


@bp.get("")
def page():
    return render_template("regra-leve3-pague2.html")


@bp.get("/api")
def api():
    return jsonify(status())
