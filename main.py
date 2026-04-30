import os
from contextlib import asynccontextmanager
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from database import init_db
from models import Link, LinkRead

load_dotenv()

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8080"))
SHORT_URL_BASE = "https://short.io/r"

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


def build_short_url(short_name: str) -> str:
    return f"{SHORT_URL_BASE}/{short_name}"


def to_link_read(link: Link) -> LinkRead:
    return LinkRead(
        id=link.id,
        original_url=link.original_url,
        short_name=link.short_name,
        short_url=build_short_url(link.short_name),
    )


@app.get("/ping")
def ping():
    return "pong"


@app.exception_handler(HTTPStatus.NOT_FOUND)
async def page_not_found(_request, _exc):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"error": "Not found"},
    )


@app.exception_handler(HTTPStatus.INTERNAL_SERVER_ERROR)
async def internal_server_error(_request, _exc):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error"},
    )


def main():
    import uvicorn

    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()
