from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException, ValidationError

from core import settings
from core import urls
from core.middlewares.settings import settings_middleware
from libs.framework_wraps.exception import http_400_error_handler, http_error_handler
import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from .config import init_config, setup, revoke


def app_install():
    app = FastAPI(
        **settings.PROJECT_DICT
    )
    # CORS
    origins = []
    # Set all CORS enabled origins

    if settings.BACKEND_CORS_ORIGINS:
        origins_raw = settings.BACKEND_CORS_ORIGINS
        for origin in origins_raw:
            use_origin = origin.strip()
            origins.append(use_origin)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    app.middleware('http')(settings_middleware(app, init_config()))
    app.add_event_handler("startup", setup)
    app.add_event_handler("shutdown", revoke)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http_400_error_handler)
    app.add_exception_handler(ValidationError, http_400_error_handler)
    app.include_router(urls.router)
    return app


async def run(app: FastAPI, host: str, port: int):
    config = Config()
    config.bind = [f"{host}:{port}"]
    config.accesslog = "-"
    config.errorlog = "-"
    shutdown_event = asyncio.Event()

    try:
        await serve(app, config, shutdown_trigger=shutdown_event.wait)  # type: ignore
    except asyncio.CancelledError:
        shutdown_event.set()
