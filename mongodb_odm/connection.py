import logging
from typing import Any, Optional, Set

from pymongo import MongoClient
from pymongo.database import Database

from .exceptions import ConnectionError, InvalidConnection
from .utils._internal_models import Connection

logger = logging.getLogger(__name__)

"""Store database connection related values in this variable"""
__connection_obj = Connection()


def _get_connection_client(url: str) -> MongoClient[Any]:
    return MongoClient(url)


def connect(url: str, databases: Optional[Set[str]] = None) -> MongoClient[Any]:
    """
    This connect function should manage and store database connection config
    that are passed by user.

    url: string type, required
        This should be a valid mongodb connection string with default database.

    databases: set of strings, optional
        values should be a set of strings that are assigned on define models.
        if a model has a value of "database" but it's not present in databases
        then the user should get an error.
    """
    global __connection_obj

    if __connection_obj.client is not None:
        """Log a warning if a user tries to connect multiple times."""
        logger.warning("Already have an connection.")
        return __connection_obj.client

    __connection_obj = Connection()

    if databases is None:
        """Assign empty set as default value"""
        databases = set()
    # get MongoClient for default connection
    client = _get_connection_client(url)
    default_database = client.get_default_database().name
    # store default database name in databases to validate later
    databases.add(default_database)

    """Store the user configuration in the global variable to use later."""
    __connection_obj.url = url
    __connection_obj.databases = databases
    __connection_obj.client = client
    logger.info("Connection established successfully")
    return __connection_obj.client


def disconnect() -> bool:
    """
    Close and clear all database connection

    Assign null to url to make sure after disconnect call
    no other database execution happens.
    """
    global __connection_obj

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
    __connection_obj = Connection()
    return True


def get_client() -> MongoClient[Any]:
    """
    Function should return MongoClient if url exists.
    Otherwise raise ConnectionError error
    """
    global __connection_obj

    if __connection_obj.client is None:
        if __connection_obj.url is not None:
            databases = __connection_obj.databases
            return connect(__connection_obj.url, databases=databases)
        else:
            raise ConnectionError("DB connection is not provided")
    else:
        return __connection_obj.client


def db(database: Optional[str] = None) -> Database[Any]:
    if database:
        """
        If a database string was passed that could be
        a default database or custom for a model
        """
        global __connection_obj
        if not __connection_obj.databases or database not in __connection_obj.databases:
            """
            Make sure valid database strings are passed
            and avoid creating invalid databases by mistake
            because mongodb creates databases on the fly.
            """
            raise InvalidConnection(f'Invalid database key was passed "{database}"')
        return get_client()[database]
    else:
        """
        If database string was not passed then return default database
        that is provided in connection url.
        """
        return get_client().get_database()


def drop_database(database: Optional[str] = None) -> None:
    db(database).command("dropDatabase")
