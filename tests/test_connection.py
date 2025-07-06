from typing import Optional

import pytest
from mongodb_odm import Document
from mongodb_odm.connection import (
    connect,
    db,
    disconnect,
    drop_database,
    get_client,
    is_async,
)
from mongodb_odm.exceptions import ConnectionError, InvalidAction, InvalidConnection
from pymongo import MongoClient
from pymongo.database import Database

from tests.constants import MONGO_URL

databases = {"logging"}


@pytest.fixture(autouse=True)
async def cleanup_connection():
    disconnect(raise_error=False)

    yield

    disconnect(raise_error=False)


def test_connection():
    client = connect(MONGO_URL)
    assert isinstance(client, MongoClient), (
        """\"connect\" function should return MongoClient object"""
    )

    client = connect(MONGO_URL, async_is_enabled=True)
    assert isinstance(client, MongoClient), (
        """\"connect\" function should return MongoClient object from previous connection even if async_is_enabled is True"""
    )


def test_disconnect():
    connect(MONGO_URL)
    disconnect()

    with pytest.raises(ConnectionError) as exc_info:
        _ = get_client()

    assert type(exc_info.value) is ConnectionError, (
        "The client should be disconnected, so it should raise ConnectionError error"
    )

    connect(MONGO_URL, async_is_enabled=True)

    with pytest.raises(InvalidAction) as exc_info:
        disconnect()


def test_get_db():
    connect(MONGO_URL)

    _db = db()
    assert isinstance(_db, Database), "db() should return a Database instance"

    _db = db(is_async_action=False)
    assert isinstance(_db, Database), (
        "db() should return a Database instance for sync action"
    )

    with pytest.raises(InvalidAction) as exc_info:
        _db = db(is_async_action=True)
    assert type(exc_info.value) is InvalidAction, (
        "db() should raise InvalidAction if is_async_action is True but client is sync"
    )


async def test_get_client_sync():
    connect(MONGO_URL)

    client = get_client()

    assert isinstance(client, MongoClient), (
        "get_client() should return a MongoClient instance"
    )


def test_get_client_sync_when_client_is_closed_but_url_exists():
    connect(MONGO_URL)

    from mongodb_odm.connection import __connection_obj

    __connection_obj.client.close()
    __connection_obj.client = None  # Simulate closed client

    client = get_client()

    assert isinstance(client, MongoClient), (
        "get_client() should return a AsyncMongoClient instance"
    )


def test_get_client_raises_connection_error():
    try:
        # Ensure we are disconnected before testing
        disconnect()
    except Exception:
        pass

    with pytest.raises(ConnectionError) as exc_info:
        get_client()

    assert isinstance(exc_info.value, ConnectionError)


def test_get_client_returns_client():
    connect(MONGO_URL)

    client = get_client()
    assert isinstance(client, MongoClient)

    disconnect()


def clean_all_database(client):
    client.get_database().command("dropDatabase")
    for database in databases:
        client[database].command("dropDatabase")


def test_multiple_database():
    class Log(Document):
        message: Optional[str] = None

        class ODMConfig:
            database = "logging"

    connect(MONGO_URL, databases=databases)
    client = get_client()
    clean_all_database(client)

    Log(message="testing multiple database").create()

    log_from_logging_db = client.logging.log.count_documents({})
    assert log_from_logging_db == 1

    log_from_default_db = client.get_database().log.count_documents({})
    assert log_from_default_db == 0

    # To fix test we have make the Log db name to None instead of "logging"
    Log.ODMConfig.database = None  # type: ignore


def test_multiple_database_invalid_database_name():
    class Log(Document):
        message: Optional[str] = None

        class ODMConfig:
            database = "log"

    with pytest.raises(InvalidConnection) as exc_info:
        connect(MONGO_URL, databases=databases)
        client = get_client()
        clean_all_database(client)

        Log(message="testing multiple database").create()

    assert type(exc_info.value) is InvalidConnection, (
        'The database name "log" is reserved for the default database'
    )

    # To fix test we have make the Log db name to None instead of "log"
    Log.ODMConfig.database = None  # type: ignore


def test_drop_database():
    connect(MONGO_URL, databases=databases)

    drop_database("logging")


def test_drop_database_with_invalid_client():
    connect(MONGO_URL, databases=databases, async_is_enabled=True)

    with pytest.raises(InvalidAction) as exc_info:
        drop_database("logging")

    assert type(exc_info.value) is InvalidAction, (
        "System should raise InvalidAction error if client is async and drop_database is called"
    )


async def test_is_async_for_sync_connection():
    with pytest.raises(ConnectionError) as exc_info:
        is_async()

    assert isinstance(exc_info.value, ConnectionError), (
        "is_async should raise ConnectionError if not connected"
    )

    connect(MONGO_URL, async_is_enabled=False)

    assert is_async() is False, "is_async should return True for async client"
