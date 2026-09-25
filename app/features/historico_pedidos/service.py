"""Regras do histórico de pedidos.

As funções de filtro recebem e devolvem listas de pedidos, sem acessar o banco.
Isso deixa a regra testável de forma isolada e mantém o core intocado: a consulta
ao banco continua sendo feita por ``list_orders``, do serviço do core.
"""

from collections.abc import Callable, Iterable

from sqlalchemy.orm import Session

from app.core.models import Order
from app.core.services.market_service import list_orders

ORDENACAO_PADRAO = "data_desc"

# chave da ordenação: (rótulo exibido, função que extrai o valor, ordem decrescente)
ORDENACOES: dict[str, tuple[str, Callable[[Order], object], bool]] = {
    "data_desc": ("Mais recentes", lambda pedido: pedido.created_at, True),
    "data_asc": ("Mais antigos", lambda pedido: pedido.created_at, False),
    "total_desc": ("Maior total", lambda pedido: pedido.total, True),
    "total_asc": ("Menor total", lambda pedido: pedido.total, False),
}


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


def ordenacao_valida(ordem: str | None) -> str:
    """Devolve a ordenação pedida, ou a padrão quando o valor é desconhecido."""
    return ordem if ordem in ORDENACOES else ORDENACAO_PADRAO


def ordenar_pedidos(pedidos: Iterable[Order], ordem: str | None) -> list[Order]:
    """Ordena por data ou por total, no sentido indicado pela chave de ordenação.

    O número do pedido desempata, para que pedidos com o mesmo valor apareçam
    sempre na mesma sequência.
    """
    _, chave, decrescente = ORDENACOES[ordenacao_valida(ordem)]
    return sorted(
        pedidos,
        key=lambda pedido: (chave(pedido), pedido.id or 0),
        reverse=decrescente,
    )


def buscar_historico(
    session: Session,
    termo: str | None = None,
    ordem: str | None = None,
) -> list[Order]:
    """Lista os pedidos do banco filtrados pelo cliente e depois ordenados.

    O filtro é aplicado antes da ordenação, então as duas coisas funcionam juntas.
    """
    return ordenar_pedidos(filtrar_por_cliente(list_orders(session), termo), ordem)
