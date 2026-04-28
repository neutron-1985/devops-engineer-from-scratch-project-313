from main import app


@app.get("/error")
def error():
    raise RuntimeError


def test_ping():
    client = app.test_client()
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.text == "pong"


def test_not_found():
    client = app.test_client()
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}


def test_internal_server_error():
    client = app.test_client()
    response = client.get("/error")

    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal server error"}
