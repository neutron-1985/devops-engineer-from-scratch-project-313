from flask import Flask

app = Flask(__name__)


@app.get("/ping")
def ping():
    return "pong"


def main():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()