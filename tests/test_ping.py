from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app


@app.get("/error")
def error():
    raise RuntimeError


def test_ping():
    client = TestClient(app)
    response = client.get("/ping")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == "pong"


def test_not_found():
    client = TestClient(app)
    response = client.get("/missing")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"error": "Not found"}


def test_internal_server_error():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/error")

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json() == {"error": "Internal server error"}
