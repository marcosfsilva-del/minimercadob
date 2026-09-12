from unittest.mock import patch

from app.core import create_app
from app.core.config import settings
from app.features.health_detalhado import service


def _client():
    app = create_app()
    return app.test_client()


def test_detailed_health_status_ok():
    """Requisito 102: cobre o status ok quando aplicacao e banco estao saudaveis."""
    response = _client().get("/api/health/detailed")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_detailed_health_returns_version_and_timestamp():
    """Requisito 102: cobre as informacoes de versao (e horario) da resposta."""
    body = _client().get("/api/health/detailed").get_json()

    assert body["version"] == settings.app_version
    assert "timestamp" in body and body["timestamp"]


def test_detailed_health_database_ok():
    """Requisito 102: cobre o cenario de sucesso da verificacao de banco."""
    body = _client().get("/api/health/detailed").get_json()

    assert body["database"] == {"status": "ok"}


def test_detailed_health_database_failure():
    """Requisito 102: cobre o cenario de falha da verificacao de banco."""
    with patch.object(
        service,
        "check_database",
        return_value={"status": "falha", "detail": "sem conexao"},
    ):
        response = _client().get("/api/health/detailed")

    body = response.get_json()
    assert response.status_code == 503
    assert body["status"] == "falha"
    assert body["database"] == {"status": "falha", "detail": "sem conexao"}
