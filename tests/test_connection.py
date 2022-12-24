import logging
from pymongo import MongoClient

from mongodb_odm.connection import connect, disconnect, force_disconnect, get_client

from .conftest import init_config, DB_URL  # noqa

logger = logging.getLogger(__name__)


def test_connection():
    client = connect(DB_URL)
    assert isinstance(
        client, MongoClient
    ), """\"connect\" function should return MongoClient object"""


def test_disconnect():
    connect(DB_URL)
    disconnect()

    client = get_client()
    """Client will be assign new connection"""
    assert isinstance(
        client, MongoClient
    ), """\"get_client\" function should return MongoClient object"""


def test_force_disconnect():
    connect(DB_URL)
    force_disconnect()

    try:
        _ = get_client()
        assert False
    except Exception as e:
        assert str(e) != "assert False"
