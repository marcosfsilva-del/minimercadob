from flask import Blueprint, jsonify, render_template

from app.features.repeat_order.service import status

bp = Blueprint("repeat_order", __name__, url_prefix="/repeat-order", template_folder="templates")


@bp.get("")
def page():
    return render_template("repeat-order.html")


@bp.get("/api")
def api():
    return jsonify(status())
