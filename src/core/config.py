import os
import logging
from core import settings
from db import models


class Config:
    TEST = {
        'database': 'test_default',
    }

    DATABASES = {
        'type': '',
        'username': '',
        'password': '',
        'host': '',
        'port': '',
        'database': '',
    }


def init_config():
    config_obj = Config()
    [
        setattr(config_obj, variable, getattr(settings, variable, ''))
        for variable in dir(settings) if
        not variable.startswith("__")
    ]
    return config_obj


async def revoke():
    logging.info("start revoke the framework")


async def register_logging():
    logging.config.dictConfig(settings.LOGGING)


async def setup():
    logging.info("start setup framework")
    from core.database import engine, BaseDatabase
    from db.models import mapper_registry
    import sqlalchemy
    mapper_registry.metadata.create_all(engine)
    metadata = sqlalchemy.MetaData(BaseDatabase)
    metadata.create_all(engine)
    await register_logging()
    logging.info("finished setup framework")


def get_dsn(config):
    assert config is not None, 'Need to inject ConfigMiddleware'

    databases = config.DATABASES.copy()
    database_user = config.DATABASES.copy()

    for key, value in database_user.items():
        if value:
            databases[key] = value
    if databases.get("type") == "sqlite":
        SQLALCHEMY_DATABASE_URI = "sqlite:///./{database}".format(database=databases.get("database"))
    else:
        SQLALCHEMY_DATABASE_URI = '{type}://{username}:{password}@{host}:{port}/{database}'.format(
            **databases
        )
    print(SQLALCHEMY_DATABASE_URI)
    return SQLALCHEMY_DATABASE_URI
