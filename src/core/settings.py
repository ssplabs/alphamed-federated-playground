from datetime import timedelta

import os
from pathlib import Path

# ~~~~~ PATH ~~~~~

BASE_DIR = Path(__file__).resolve().parent.parent

# ~~~~~ DATA_BASE ~~~~~

DATABASES = {
    'type': os.environ.get('type', 'sqlite'),
    'database': os.environ.get('database', 'federated.db')
}

# ~~~~~ SECRET ~~~~~
SECRET_KEY = ")h3kjq5t@udh59^wpszq4r@9dd=r-c)!"

if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

# ~~~~~ JWT ~~~~~
JWT_EXPIRATION_DELTA = timedelta(hours=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 10)))  # in hours
JWT_REFRESH_EXPIRATION_DELTA = timedelta(hours=int(os.getenv('JWT_REFRESH_EXPIRATION_DELTA', 10)))  # in hours
JWT_AUTH_HEADER_PREFIX = os.getenv('JWT_AUTH_HEADER_PREFIX', 'JWT')
JWT_SECRET_KEY = SECRET_KEY

# ~~~~~ CORS ~~~~~

# BACKEND_CORS_ORIGINS = os.getenv('BACKEND_CORS_ORIGINS')
BACKEND_CORS_ORIGINS = [
    "*"
]
# a list of origins separated by commas, e.g: ['http://localhost', 'http://localhost:4200', 'http://localhost:3000']

# ~~~~~ APP ~~~~~
PROJECT_NAME = "alphamed-federated-playground"

PROJECT_DICT = {
    "title": """
alphamed-federated-playground
""",
    "description": PROJECT_NAME,
    "version": "1.0.0",
    "openapi_url": "/fed-playground/api/openapi.json",
    "docs_url": "/fed-playground/api/~/swagger",
    "redoc_url": "/fed-playground/api/~/redoc",

}

# ~~~~~ LOGGING ~~~~~

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'app': {
            'format': '%(asctime)s|{version}|%(levelname)s|%(process)d|%(module)s|%(funcName)s|%(lineno)d|%(message)s'.format(
                version=1),
        },
        'access': {
            'format': '%(asctime)s|{version}|%(levelname)s|%(message)s'.format(version=1)
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'access': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'access.log'),
            'formatter': 'access',
        },
        'app': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'app.log'),
            'formatter': 'app',
        },
        'debug': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'formatter': 'access',
        },
        'error': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'error.log'),
            'formatter': 'app',
            'level': 'ERROR',
        }
    },
    'loggers': {
        'asyncio': {
            'handlers': ['app', 'console', 'error'],
            'level': 'WARN',
        },
        'access': {
            'handlers': ['access'],
            'level': 'INFO',
        },
        'app': {
            'handlers': ['app', 'error', 'console'],
            'level': 'INFO',
        },
        'debug': {
            'handlers': ['debug'],
            'level': 'INFO',
        }
    },
}
