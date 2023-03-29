import logging

from mongodb_odm.connection import connect, disconnect, get_client
from pymongo import MongoClient

from .conftest import DB_URL, init_config  # noqa

logger = logging.getLogger(__name__)


def test_connection():
    disconnect()  # first disconnect init_config connection

    client = connect(DB_URL)
    assert isinstance(
        client, MongoClient
    ), """\"connect\" function should return MongoClient object"""


def test_disconnect():
    disconnect()  # first disconnect init_config connection

    disconnect()  # try to cover warning log

    connect(DB_URL)
    disconnect()

    try:
        _ = get_client()
        assert False
    except Exception as e:
        assert str(e) != "assert False"


def test_get_client():
    disconnect()  # first disconnect init_config connection

    try:
        print(get_client())
        assert False
    except Exception as e:
        assert str(e) != "assert False"
