from datetime import datetime, timezone

from app.core.config import settings


def get_detailed_health() -> dict:
    """Monta o payload do health detalhado da aplicacao.

    Requisito 100: status da aplicacao, versao e horario da resposta.
    """
    return {
        "status": "ok",
        "version": settings.app_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
