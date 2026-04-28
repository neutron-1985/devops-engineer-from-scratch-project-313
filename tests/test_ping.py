from http import HTTPStatus

from main import app


@app.get("/error")
def error():
    raise RuntimeError


def test_ping():
    client = app.test_client()
    response = client.get("/ping")

    assert response.status_code == HTTPStatus.OK
    assert response.text == "pong"


def test_not_found():
    client = app.test_client()
    response = client.get("/missing")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == {"error": "Not found"}


def test_internal_server_error():
    client = app.test_client()
    response = client.get("/error")

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == {"error": "Internal server error"}
