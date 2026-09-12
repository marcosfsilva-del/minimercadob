from flask import Blueprint, jsonify

from app.features.health_detalhado.service import get_detailed_health

health_detalhado_bp = Blueprint(
    "health_detalhado",
    __name__,
    url_prefix="/api/health",
)


@health_detalhado_bp.get("/detailed")
def detailed():
    payload = get_detailed_health()
    status_code = 200 if payload["status"] == "ok" else 503
    return jsonify(payload), status_code
