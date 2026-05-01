import os
from contextlib import asynccontextmanager
from http import HTTPStatus

import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from sqlmodel import SQLModel, create_engine

from database import get_database_url
from models import Link, LinkCreate, LinkShow, LinkUpdate
from repositories import LinksRepository

load_dotenv()

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8080"))
SENTRY_DSN = os.environ.get("SENTRY_DSN")
SHORT_URL_BASE = os.environ.get("SHORT_URL_BASE", "https://short.io/r")

if SENTRY_DSN:
    if os.getenv("APP_ENV") != "test":
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            send_default_pii=True,
        )

engine = create_engine(get_database_url())
links_repository = LinksRepository(engine)

def init_db():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(HTTPStatus.NOT_FOUND)
async def page_not_found(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "Страница не найдена",
            "path": str(request.url),
        },
    )

@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Что-то пошло не так"
        },
    )

@app.get("/ping")
def ping():
    return "pong"

@app.get("/boom")
async def boom():
    raise RuntimeError()

@app.get("/sentry-debug")
async def trigger_error1():
    return "issue resolved"

def build_link_show(link: Link):
    return LinkShow(
        id=link.id,
        original_url=link.original_url,
        short_name=link.short_name,
        short_url=f"{SHORT_URL_BASE}/{link.short_name}",
    )

@app.get("/api/links", response_model=list[LinkShow])
def get_links():
    links = links_repository.get_all()
    return [
        build_link_show(link)
        for link in links
    ]

@app.post("/api/links")
def create_link(link: LinkCreate):
    existing_link = links_repository.get_by_short_name(link.short_name)
    if existing_link is not None:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)

    return links_repository.create(link)

@app.get("/api/links/{link_id}", response_model=LinkShow)
def get_link(link_id: int):
    link = links_repository.get_by_id(link_id)
    if link is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return build_link_show(link)

@app.post("/api/links/{link_id}", response_model=LinkShow)
def edit_link(link_id: int, link_update: LinkUpdate):
    link = links_repository.get_by_id(link_id)
    if link is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    updated_link = links_repository.update(link, link_update)
    return build_link_show(updated_link)

@app.delete("/api/links/{link_id}")
def delete_link(link_id: int):
    link = links_repository.get_by_id(link_id)
    if link is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    links_repository.delete(link)
    return Response(status_code=HTTPStatus.NO_CONTENT)

def main():
    import uvicorn

    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()
