from app.core import create_app
from app.features.app_version.service import version_info


def test_version_info_retorna_campos_da_configuracao():
    resultado = version_info()

    assert set(resultado) == {"app_version", "commit_sha"}


def test_endpoint_version_retorna_json():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/version")

    assert response.status_code == 200
    assert response.get_json() == version_info()