import uuid

from app.core import create_app


def test_cada_request_recebe_request_id_no_header():
    client = create_app().test_client()

    response = client.get("/api/health")

    request_id = response.headers.get("X-Request-ID")
    assert request_id
    uuid.UUID(request_id)


def test_requests_diferentes_recebem_ids_diferentes():
    client = create_app().test_client()

    primeiro = client.get("/api/health").headers["X-Request-ID"]
    segundo = client.get("/api/health").headers["X-Request-ID"]

    assert primeiro != segundo


def test_reutiliza_request_id_enviado_pelo_cliente():
    client = create_app().test_client()

    response = client.get("/api/health", headers={"X-Request-ID": "meu-id-123"})

    assert response.headers["X-Request-ID"] == "meu-id-123"
