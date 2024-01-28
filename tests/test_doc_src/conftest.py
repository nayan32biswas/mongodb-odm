import importlib
import os

import pytest
from mongodb_odm.connection import disconnect, drop_database

DB_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb")


@pytest.fixture
def setup_test_database():
    """First force to reimport all modules to remove preloaded models"""
    module_to_reload = importlib.import_module("mongodb_odm")
    importlib.reload(module_to_reload)

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
