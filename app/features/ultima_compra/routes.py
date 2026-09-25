from flask import Blueprint, jsonify, render_template

from app.features.ultima_compra.service import status

bp = Blueprint("ultima_compra", __name__, url_prefix="/ultima-compra", template_folder="templates")


@bp.get("")
def page():
    return render_template("ultima-compra.html")


@bp.get("/api")
def api():
    return jsonify(status())
