import asyncio

import pytest
from mongodb_odm import adisconnect, connect, disconnect
from mongodb_odm.connection import db

from tests.constants import CONNECTION_POOL_PARAMS, MONGO_URL

INIT_CONFIG = "init_config"
ASYNC_INIT_CONFIG = "async_init_config"


@pytest.fixture(scope="session")
def event_loop():
    """Force a single event loop for all async tests in this session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def database_connection():
    connect(MONGO_URL, connection_kwargs=CONNECTION_POOL_PARAMS)

    yield None

    disconnect()


@pytest.fixture()
def init_config(database_connection):
    db().command("dropDatabase")

    yield None

    db().command("dropDatabase")


@pytest.fixture()
async def async_init_config():
    # Due to asyncio event loop restrictions, we need to open new connections for each async test
    connect(MONGO_URL, connection_kwargs=CONNECTION_POOL_PARAMS, async_is_enabled=True)
    await db().command("dropDatabase")

    yield None

    await db().command("dropDatabase")
    # We need to disconnect the async client after the test so that new connections can be established in the next async test
    await adisconnect()
