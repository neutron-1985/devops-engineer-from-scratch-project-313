from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app


def test_ping():
    client = TestClient(app)
    response = client.get("/ping")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == "pong"
