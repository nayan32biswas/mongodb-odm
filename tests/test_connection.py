from typing import Optional

from mongodb_odm import Document
from mongodb_odm.connection import connect, disconnect, get_client
from pymongo import MongoClient

from tests.conftest import MONGO_URL

databases = {"logging"}


def test_connection():
    client = connect(MONGO_URL)
    assert isinstance(client, MongoClient), (
        """\"connect\" function should return MongoClient object"""
    )


def test_disconnect():
    disconnect()  # try to cover warning log

    connect(MONGO_URL)
    disconnect()

    try:
        _ = get_client()
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_get_client():
    try:
        print(get_client())
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


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

    try:
        connect(MONGO_URL, databases=databases)
        client = get_client()
        clean_all_database(client)

        Log(message="testing multiple database").create()
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""

    # To fix test we have make the Log db name to None instead of "log"
    Log.ODMConfig.database = None  # type: ignore
