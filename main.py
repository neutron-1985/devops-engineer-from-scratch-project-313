from http import HTTPStatus

from flask import Flask, jsonify

app = Flask(__name__)


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
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
