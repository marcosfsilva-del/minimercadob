from datetime import datetime, timezone

from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine


def check_database() -> dict:
    """Verifica a conexao com o banco SQLite configurado.

    Requisito 101: indica "ok" quando a conexao responde e "falha"
    quando a verificacao levanta qualquer excecao.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as exc:  # reportamos qualquer falha de conexao com o banco
        return {"status": "falha", "detail": str(exc)}


def get_detailed_health() -> dict:
    """Monta o payload do health detalhado da aplicacao.

    Requisito 100: status da aplicacao, versao e horario da resposta.
    Requisito 101: soma a verificacao de banco. Se o banco falhar, o
    status geral da aplicacao tambem reflete a falha.
    """
    database = check_database()
    status = "ok" if database["status"] == "ok" else "falha"
    return {
        "status": status,
        "version": settings.app_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": database,
    }
