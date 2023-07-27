import logging
from typing import Any, Optional, Set

from pymongo import MongoClient
from pymongo.database import Database

from .exceptions import ConnectionExist, InvalidConnection
from .utils._internal_models import Connection

logger = logging.getLogger(__name__)


__connection_obj = Connection()


def _get_connection_client(url: str) -> MongoClient[Any]:
    return MongoClient(url)


def connect(url: str, databases: Optional[Set[str]] = None) -> MongoClient[Any]:
    if __connection_obj.client is not None:
        logger.warning("Already have an connection.")
        return __connection_obj.client

    if databases is None:
        databases = set()
    client = _get_connection_client(url)
    default_database = client.get_default_database().name
    databases.add(default_database)

    __connection_obj.url = url
    __connection_obj.databases = databases
    __connection_obj.client = client
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


def db(database: Optional[str] = None) -> Database[Any]:
    if database:
        if not __connection_obj.databases or database not in __connection_obj.databases:
            raise InvalidConnection(f'Invalid database key was passed "{database}"')
        return get_client()[database]
    else:
        return get_client().get_database()
