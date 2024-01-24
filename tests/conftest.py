import os

import pytest
from mongodb_odm import connect, disconnect
from mongodb_odm.connection import db

DB_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb")


@pytest.fixture(autouse=True)
def init_config():
    print(DB_URL)
    connect(DB_URL)
    db().command("dropDatabase")
    yield None
    disconnect()
