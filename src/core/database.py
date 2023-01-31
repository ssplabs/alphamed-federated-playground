# -*- coding: utf-8 -*-
from core.config import init_config, get_dsn
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.sql import sqltypes
from sqlalchemy import Column


@as_declarative()
class BaseDatabase(object):

    @declared_attr
    def __tableName__(cls):
        return cls.__name__.lower()

    id = Column(sqltypes.BigInteger, primary_key=True)


app_config = init_config()

dsn = get_dsn(app_config)
engine = create_engine(dsn, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
