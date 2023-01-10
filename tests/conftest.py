import os
import pytest

from mongodb_odm.connection import connect

DB_URL = os.environ.get(
    "TEST_MONGO_HOST",
    "mongodb://root:password@db:27017/test?authSource=admin",
)


@pytest.fixture(autouse=True)
def init_config():
    connect(DB_URL)
    yield None
    # disconnect()
