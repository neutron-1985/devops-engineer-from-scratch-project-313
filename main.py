import os
from contextlib import asynccontextmanager
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse

import links_repository
from database import init_db
from models import LinkCreate, LinkRead, LinkUpdate

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


def to_link_read(link) -> LinkRead:
    return LinkRead(
        id=link.id,
        original_url=link.original_url,
        short_name=link.short_name,
        short_url=build_short_url(link.short_name),
    )


@app.get("/ping")
def ping():
    return "pong"


@app.get("/api/links")
def get_links():
    links = links_repository.get_links()
    return [to_link_read(link) for link in links]


@app.post("/api/links")
def create_link(link_create: LinkCreate):
    links_repository.create_link(link_create.original_url, link_create.short_name)
    return Response(status_code=HTTPStatus.CREATED)


@app.get("/api/links/{link_id}")
def get_link(link_id: int):
    link = links_repository.get_link(link_id)

    if link is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return to_link_read(link)


@app.put("/api/links/{link_id}")
def update_link(link_id: int, link_update: LinkUpdate):
    link = links_repository.update_link(
        link_id,
        link_update.original_url,
        link_update.short_name,
    )

    if link is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return to_link_read(link)


@app.delete("/api/links/{link_id}")
def delete_link(link_id: int):
    is_deleted = links_repository.delete_link(link_id)

    if not is_deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return Response(status_code=HTTPStatus.NO_CONTENT)


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
