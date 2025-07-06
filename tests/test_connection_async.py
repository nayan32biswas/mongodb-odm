from typing import Optional

import pytest
from mongodb_odm import Document
from mongodb_odm.connection import (
    adisconnect,
    adrop_database,
    connect,
    db,
    get_client,
    is_async,
)
from mongodb_odm.exceptions import ConnectionError, InvalidAction, InvalidConnection
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from tests.constants import MONGO_URL

databases = {"logging"}


@pytest.fixture(autouse=True)
async def cleanup_connection():
    await adisconnect(raise_error=False)

    yield

    await adisconnect(raise_error=False)


async def test_connection():
    client = connect(MONGO_URL, async_is_enabled=True)
    assert isinstance(client, AsyncMongoClient), (
        """\"connect\" function should return AsyncMongoClient object"""
    )

    client = connect(MONGO_URL, async_is_enabled=False)
    assert isinstance(client, AsyncMongoClient), (
        """\"connect\" function should return AsyncMongoClient object from previous connection even if async_is_enabled is False"""
    )


async def test_disconnect():
    connect(MONGO_URL, async_is_enabled=True)
    await adisconnect()

    with pytest.raises(ConnectionError) as exc_info:
        _ = get_client()

    assert type(exc_info.value) is ConnectionError, (
        "The client should be disconnected, so it should raise ConnectionError error"
    )

    connect(MONGO_URL, async_is_enabled=False)

    with pytest.raises(InvalidAction) as exc_info:
        await adisconnect()


async def test_get_db_async():
    connect(MONGO_URL, async_is_enabled=True)

    _db = db()
    assert isinstance(_db, AsyncDatabase), "db() should return a AsyncDatabase instance"

    _db = db(is_async_action=True)
    assert isinstance(_db, AsyncDatabase), (
        "db() should return a AsyncDatabase instance for sync action"
    )

    with pytest.raises(InvalidAction) as exc_info:
        _db = db(is_async_action=False)
    assert type(exc_info.value) is InvalidAction, (
        "db() should raise InvalidAction if is_async_action is True but client is sync"
    )


async def test_get_client_async():
    connect(MONGO_URL, async_is_enabled=True)

    client = get_client()

    assert isinstance(client, AsyncMongoClient), (
        "get_client() should return a AsyncMongoClient instance"
    )


async def test_get_client_async_when_client_is_closed_but_url_exists():
    connect(MONGO_URL, async_is_enabled=True)

    from mongodb_odm.connection import __connection_obj

    await __connection_obj.client.close()
    __connection_obj.client = None  # Simulate closed client

    client = get_client()

    assert isinstance(client, AsyncMongoClient), (
        "get_client() should return a AsyncMongoClient instance"
    )


async def test_get_client_raises_connection_error():
    with pytest.raises(ConnectionError) as exc_info:
        get_client()

    assert isinstance(exc_info.value, ConnectionError)


async def test_get_client_returns_client():
    connect(MONGO_URL, async_is_enabled=True)

    client = get_client()
    assert isinstance(client, AsyncMongoClient)

    await adisconnect()


async def clean_all_database(client):
    await client.get_database().command("dropDatabase")
    for database in databases:
        await client[database].command("dropDatabase")


async def test_multiple_database():
    class Log(Document):
        message: Optional[str] = None

        class ODMConfig:
            database = "logging"

    connect(MONGO_URL, databases=databases, async_is_enabled=True)
    client = get_client()
    await clean_all_database(client)

    _ = await Log(message="testing multiple database").acreate()

    log_from_logging_db = await client.logging.log.count_documents({})
    assert log_from_logging_db == 1

    log_from_default_db = await client.get_database().log.count_documents({})
    assert log_from_default_db == 0

    # To fix test we have make the Log db name to None instead of "logging"
    Log.ODMConfig.database = None  # type: ignore


async def test_multiple_database_invalid_database_name():
    class Log(Document):
        message: Optional[str] = None

        class ODMConfig:
            database = "log"

    with pytest.raises(InvalidConnection) as exc_info:
        connect(MONGO_URL, databases=databases, async_is_enabled=True)
        client = get_client()
        await clean_all_database(client)

        _ = await Log(message="testing multiple database").acreate()

    assert type(exc_info.value) is InvalidConnection, (
        'The database name "log" is reserved for the default database'
    )

    # To fix test we have make the Log db name to None instead of "log"
    Log.ODMConfig.database = None  # type: ignore


async def test_adrop_database():
    connect(MONGO_URL, databases=databases, async_is_enabled=True)

    await adrop_database("logging")


async def test_adrop_database_with_invalid_client():
    connect(MONGO_URL, databases=databases, async_is_enabled=False)

    with pytest.raises(InvalidAction) as exc_info:
        await adrop_database("logging")

    assert type(exc_info.value) is InvalidAction, (
        "System should raise InvalidAction error if client is async and drop_database is called"
    )


async def test_is_async_for_async_connection():
    with pytest.raises(ConnectionError) as exc_info:
        is_async()

    assert isinstance(exc_info.value, ConnectionError), (
        "is_async should raise ConnectionError if not connected"
    )

    connect(MONGO_URL, async_is_enabled=True)

    assert is_async() is True, "is_async should return True for async client"
