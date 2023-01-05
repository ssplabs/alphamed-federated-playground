# -*- coding: utf-8 -*-
import logging
from starlette.requests import Request
from core.database import engine, SessionLocal

_logger = logging.getLogger("app")


def get_database(request: Request):
    local_db = SessionLocal()
    try:
        yield local_db
        local_db.commit()
    except Exception as e:
        local_db.rollback()
        _logger.exception(e)
    finally:
        local_db.close()

