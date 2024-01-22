import os

import pytest
from mongodb_odm import connect, disconnect
from mongodb_odm.connection import drop_database

DB_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb")


@pytest.fixture(autouse=True)
def init_config():
    print(DB_URL)
    connect(DB_URL)
    drop_database()
    yield None
    disconnect()
