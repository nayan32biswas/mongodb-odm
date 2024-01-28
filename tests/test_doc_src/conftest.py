import os

import pytest
from mongodb_odm.connection import disconnect, drop_database

DB_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb")


@pytest.fixture
def setup_test_database():
    try:
        drop_database()
        drop_database("logging")
    except Exception:
        pass
    try:
        disconnect()
    except Exception:
        pass

    yield None

    try:
        disconnect()
    except Exception:
        pass
