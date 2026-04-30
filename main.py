import os
from contextlib import asynccontextmanager
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse

import links_repository
from database import init_db
from links_repository import ShortNameAlreadyExistsError
from models import LinkCreate, LinkRead, LinkUpdate

load_dotenv()

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8080"))
SHORT_URL_BASE = os.environ.get("SHORT_URL_BASE", "https://short.io/r")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


def build_short_url(short_name):
    return f"{SHORT_URL_BASE.rstrip('/')}/{short_name}"


def to_link_read(link):
    return LinkRead(
        id=link.id,
        original_url=link.original_url,
        short_name=link.short_name,
        created_at=link.created_at,
        short_url=build_short_url(link.short_name),
    )


def short_name_conflict_response():
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={"error": "Short name already exists"},
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
    try:
        link = links_repository.create_link(
            link_create.original_url,
            link_create.short_name,
        )
    except ShortNameAlreadyExistsError:
        return short_name_conflict_response()

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content=to_link_read(link).model_dump(mode="json"),
    )


@app.get("/api/links/{link_id}")
def get_link(link_id: int):
    link = links_repository.get_link(link_id)

    if link is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return to_link_read(link)


@app.put("/api/links/{link_id}")
def update_link(link_id: int, link_update: LinkUpdate):
    try:
        link = links_repository.update_link(
            link_id,
            link_update.original_url,
            link_update.short_name,
        )
    except ShortNameAlreadyExistsError:
        return short_name_conflict_response()

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
