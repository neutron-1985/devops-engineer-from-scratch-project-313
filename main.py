import os
from http import HTTPStatus

from flask import Flask, jsonify

app = Flask(__name__)

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8080"))


@app.get("/ping")
def ping():
    return "pong"


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    return jsonify(error="Not found"), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    return (
        jsonify(error="Internal server error"),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def main():
    app.run(host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()
