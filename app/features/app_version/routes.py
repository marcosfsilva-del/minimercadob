from flask import Blueprint, jsonify, render_template

from app.features.app_version.service import version_info

bp = Blueprint("app_version", __name__, template_folder="templates")


@bp.get("/app-version")
def page():
    return render_template("app-version.html", **version_info())


@bp.get("/api/version")
def api():
    return jsonify(version_info())