import os
import logging
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import FastAPI, Request, logger
from fastapi.responses import JSONResponse

load_dotenv()

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8080"))


app = FastAPI()
logger = logging.getLogger(__name__)

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
    logger.exception("Unhandled internal error")
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


def main():
    import uvicorn

    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()
