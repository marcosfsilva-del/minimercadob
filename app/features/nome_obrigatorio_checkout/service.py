MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 60


def status() -> dict[str, str]:
    return {"feature": "nome-obrigatorio-checkout", "status": "ok"}


def validate_customer_name(raw_name: str | None) -> str:
    name = (raw_name or "").strip()
    if not name:
        raise ValueError("Informe o nome do cliente para finalizar o pedido.")
    if len(name) < MIN_NAME_LENGTH:
        raise ValueError(f"Nome muito curto. Use pelo menos {MIN_NAME_LENGTH} caracteres.")
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Nome muito longo. Use no máximo {MAX_NAME_LENGTH} caracteres.")
    return name
