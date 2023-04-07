import logging
from typing import Any

from pymongo import MongoClient
from pymongo.database import Database

from .exceptions import ConnectionExist
from .utils._internal_models import Connection

logger = logging.getLogger(__name__)


__connection_obj = Connection()


def _get_connection_client(url: str) -> MongoClient[Any]:
    return MongoClient(url)


def connect(url: str) -> MongoClient[Any]:
    if __connection_obj.client is not None:
        logger.warning("Already have an connection.")
        return __connection_obj.client
    __connection_obj.url = url
    __connection_obj.client = _get_connection_client(url)
    logger.info("Connection established successfully")
    return __connection_obj.client


def disconnect() -> bool:
    if __connection_obj.client:
        __connection_obj.client.close()
        __connection_obj.client = None
    else:
        logger.warning("No client connection found")
    if __connection_obj.url:
        __connection_obj.url = None
    else:
        logger.warning("No connection URL found.")
    logger.info("Disconnect the db connection")

    from .models import _clear_cache

    _clear_cache()
    return True


def get_client() -> MongoClient[Any]:
    if __connection_obj.client is None:
        if __connection_obj.url is not None:
            return connect(__connection_obj.url)
        else:
            raise ConnectionExist("DB connection is not provided")
    else:
        return __connection_obj.client


def db() -> Database[Any]:
    return get_client().get_database()
