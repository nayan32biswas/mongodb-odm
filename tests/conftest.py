import os
import pytest

from mongodb_odm.connection import connect

DB_URL = os.environ.get(
    "MONGO_HOST",
    "mongodb://root:password@localhost:27017/test?authSource=admin",
)


@pytest.fixture(autouse=True)
def init_config():
    connect(DB_URL)
    yield None
    # disconnect()
