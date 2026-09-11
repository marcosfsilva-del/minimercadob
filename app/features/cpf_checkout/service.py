import re

from app.core.models import Customer
from app.core.services.market_service import create_order


def validar_cpf(cpf: str) -> str:
    cpf = cpf.strip()
    if not re.fullmatch(r"[0-9]{11}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}", cpf):
        raise ValueError("informe um cpf com 11 dígitos, com ou sem pontuação.")
    return cpf.replace(".", "").replace("-", "")


def criar_pedido_com_cpf(db, items, nome, cpf):
    cpf = validar_cpf(cpf)
    pedido = create_order(db, items, nome)
    db.add(Customer(name=nome or "cliente", cpf=cpf))
    db.flush()
    return pedido
