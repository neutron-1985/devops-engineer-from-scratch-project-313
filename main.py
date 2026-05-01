import logging
import os
from http import HTTPStatus

import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

load_dotenv()

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8080"))
SENTRY_DSN = os.environ.get("SENTRY_DSN")

if SENTRY_DSN:
    if os.getenv("APP_ENV") != "test":
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            # Add data like request headers and IP for users,
            # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
            send_default_pii=True,
        )

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
    sentry_sdk.capture_exception(exc)
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

@app.get("/sentry-debug")
async def trigger_error1():
    return "issue resolved"

@app.get("/sentry-debug2")
async def trigger_error2():
    return 10 / 0

@app.get("/sentry-no-more")
async def trigger_error3():
    return "issue resolved"

def main():
    import uvicorn

    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()
