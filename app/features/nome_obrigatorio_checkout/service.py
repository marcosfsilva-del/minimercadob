def status() -> dict[str, str]:
    return {"feature": "nome-obrigatorio-checkout", "status": "ok"}


def validate_customer_name(raw_name: str | None) -> str:
    name = (raw_name or "").strip()
    if not name:
        raise ValueError("Informe o nome do cliente para finalizar o pedido.")
    return name
