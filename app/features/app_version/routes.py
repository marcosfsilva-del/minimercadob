from flask import Blueprint, jsonify, render_template

from app.features.app_version.service import status

bp = Blueprint("app_version", __name__, url_prefix="/app-version", template_folder="templates")


@bp.get("")
def page():
    return render_template("app-version.html")


@bp.get("/api")
def api():
    return jsonify(status())
