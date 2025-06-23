import os

import pytest
from mongodb_odm import adisconnect, connect, disconnect
from mongodb_odm.connection import db

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb")

INIT_CONFIG = "init_config"
ASYNC_INIT_CONFIG = "async_init_config"


@pytest.fixture()
def init_config():
    connect(MONGO_URL)
    db().command("dropDatabase")

    yield None

    disconnect()


@pytest.fixture()
async def async_init_config():
    connect(MONGO_URL, async_is_enabled=True)
    await db().command("dropDatabase")

    yield None

    await adisconnect()
