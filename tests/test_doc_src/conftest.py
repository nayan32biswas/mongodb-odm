import pytest
from mongodb_odm.connection import connect, disconnect

from tests.constants import MONGO_URL
from tests.utils import drop_all_user_databases

SETUP_TEST_DATABASE = "setup_test_database"


@pytest.fixture
def setup_test_database():
    client = connect(MONGO_URL)
    drop_all_user_databases(client)
    disconnect()

    yield None

    try:
        disconnect()
    except Exception:
        pass
