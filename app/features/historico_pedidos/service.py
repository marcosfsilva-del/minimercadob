"""Regras do histórico de pedidos.

As funções de filtro recebem e devolvem listas de pedidos, sem acessar o banco.
Isso deixa a regra testável de forma isolada e mantém o core intocado: a consulta
ao banco continua sendo feita por ``list_orders``, do serviço do core.
"""

from collections.abc import Iterable

from sqlalchemy.orm import Session

from app.core.models import Order
from app.core.services.market_service import list_orders


def status() -> dict[str, str]:
    return {"feature": "historico-pedidos", "status": "ok"}


def normalizar_termo(termo: str | None) -> str:
    """Remove espaços das pontas e ignora diferença entre maiúsculas e minúsculas."""
    return (termo or "").strip().casefold()


def filtrar_por_cliente(pedidos: Iterable[Order], termo: str | None) -> list[Order]:
    """Mantém os pedidos cujo nome do cliente contém o termo informado.

    Termo vazio ou só com espaços devolve todos os pedidos. Pedido sem nome de
    cliente só aparece quando não há termo de busca.
    """
    busca = normalizar_termo(termo)
    pedidos = list(pedidos)
    if not busca:
        return pedidos
    return [
        pedido
        for pedido in pedidos
        if busca in (pedido.customer_name or "").casefold()
    ]


def buscar_historico(session: Session, termo: str | None = None) -> list[Order]:
    """Lista os pedidos do banco já filtrados pelo nome do cliente."""
    return filtrar_por_cliente(list_orders(session), termo)
