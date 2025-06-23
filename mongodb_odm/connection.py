import logging
from typing import Any, Optional, Set, Union

from mongodb_odm.exceptions import ConnectionError, InvalidAction, InvalidConnection
from mongodb_odm.utils._internal_models import Connection
from pymongo import AsyncMongoClient, MongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.database import Database

logger = logging.getLogger(__name__)

"""Store database connection related values in this variable"""
__connection_obj = Connection()


def _get_connection_client(url: str) -> MongoClient[Any]:
    return MongoClient(url)


def _get_async_connection_client(url: str) -> AsyncMongoClient[Any]:
    return AsyncMongoClient(url)


def connect(
    url: str, databases: Optional[Set[str]] = None, async_is_enabled: bool = False
) -> Union[AsyncMongoClient[Any], MongoClient[Any]]:
    """
    This connect function should manage and store database connection config
    that are passed by user.

    url: string type, required
        This should be a valid mongodb connection string with default database.

    databases: set of strings, optional
        values should be a set of strings that are assigned on define models.
        The value is meant to validate that user is not trying to connect
        to a database that is not defined in the models.

    async_is_enabled: bool, optional
        If True then use AsyncMongoClient, otherwise use MongoClient.
        Default is False.
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

    client: Union[AsyncMongoClient[Any], MongoClient[Any]]
    if async_is_enabled:
        client = _get_async_connection_client(url)
    else:
        client = _get_connection_client(url)

    default_database = client.get_default_database().name
    databases.add(default_database)

    """Store the user configuration in the global variable to use later."""
    __connection_obj.url = url
    __connection_obj.databases = databases
    __connection_obj.client = client
    __connection_obj.async_is_enabled = async_is_enabled

    logger.info("Connection established successfully")

    return __connection_obj.client


def _disconnect_common() -> bool:
    global __connection_obj

    if __connection_obj.url:
        __connection_obj.url = None
    else:
        logger.warning("No connection URL found.")

    logger.info("Disconnect the db connection")

    from mongodb_odm.models import _clear_cache

    _clear_cache()

    result = Connection()
    __connection_obj = result

    return True


def disconnect() -> bool:
    global __connection_obj

    if __connection_obj.client is None:
        logger.warning("No client connection found")
        return _disconnect_common()

    if isinstance(__connection_obj.client, AsyncMongoClient):
        raise InvalidAction(
            "The client is configured as async. Use adisconnect() instead."
        )

    __connection_obj.client.close()
    __connection_obj.client = None

    return _disconnect_common()


async def adisconnect() -> bool:
    global __connection_obj

    if __connection_obj.client is None:
        logger.warning("No client connection found")
        return _disconnect_common()

    if isinstance(__connection_obj.client, MongoClient):
        raise InvalidAction(
            "The client is configured as sync. Use disconnect() instead."
        )

    await __connection_obj.client.close()
    __connection_obj.client = None

    return _disconnect_common()


def get_client() -> Union[AsyncMongoClient[Any] | MongoClient[Any]]:
    """
    Function should return MongoClient if url exists.
    Otherwise raise ConnectionError error
    """
    global __connection_obj

    if __connection_obj.client:
        return __connection_obj.client

    if __connection_obj.url is None:
        raise ConnectionError("DB connection URL is not provided")

    databases = __connection_obj.databases
    async_is_enabled = __connection_obj.async_is_enabled

    return connect(
        __connection_obj.url,
        databases=databases,
        async_is_enabled=async_is_enabled,
    )


def db(
    database: Optional[str] = None,
    is_async_action: Optional[bool] = None,
) -> Union[Database[Any], AsyncDatabase[Any]]:
    global __connection_obj

    if is_async_action is None:
        is_async_action = __connection_obj.async_is_enabled

    client = get_client()

    if isinstance(client, MongoClient) and is_async_action is True:
        raise InvalidAction("The client is not configured as async")
    elif isinstance(client, AsyncMongoClient) and is_async_action is False:
        raise InvalidAction("The client is not configured as sync")

    if database:
        if not __connection_obj.databases or database not in __connection_obj.databases:
            """
            Make sure valid database strings are passed
            and avoid creating invalid databases by mistake
            because mongodb creates databases on the fly.
            """
            raise InvalidConnection(f'Invalid database key was passed "{database}"')

        return client[database]
    else:
        """
        If database string was not passed then return default database
        that is provided in connection url.
        """
        return client.get_database()


def drop_database(database: Optional[str] = None) -> None:
    collection = db(database)
    if not isinstance(collection, Database):
        raise InvalidAction(
            "The client is not configured as sync please use 'adrop_database' instead."
        )

    collection.command("dropDatabase")


async def adrop_database(database: Optional[str] = None) -> None:  # noqa
    collection = db(database, is_async_action=True)
    if not isinstance(collection, AsyncDatabase):
        raise InvalidAction(
            "The client is not configured as async please use 'drop_database' instead."
        )

    await collection.command("dropDatabase")


async def is_async() -> bool:
    global __connection_obj
    if not __connection_obj.client:
        raise ConnectionError("No connection established. Please connect first.")

    return isinstance(__connection_obj.client, AsyncMongoClient)
