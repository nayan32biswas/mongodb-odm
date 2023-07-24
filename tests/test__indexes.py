import logging
from datetime import datetime
from typing import List, Optional

from mongodb_odm import ASCENDING, Document, Field, IndexModel, connect, disconnect
from mongodb_odm.utils.apply_indexes import apply_indexes

from .conftest import DB_URL, init_config  # noqa

databases = {"logging"}
logger = logging.getLogger(__name__)


class TestIndexes(Document):
    username: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config(Document.Config):
        collection_name = "test_indexes"
        indexes = [
            IndexModel([("username", ASCENDING)], unique=True),
        ]


def test_create_indexes_without_connection():
    disconnect()

    try:
        apply_indexes()
        assert False
    except Exception as e:
        assert str(e) != "assert False"


def test_no_index_change():
    apply_indexes()

    apply_indexes()  # No index was changed


def check_indexes(index_keys: List[str]):
    for i, index in enumerate(TestIndexes._get_collection().list_indexes()):
        assert index_keys[i] in index.to_dict()["key"]  # type: ignore
    return True


def test_create_indexes():
    TestIndexes.Config.indexes = [  # type: ignore
        IndexModel([("username", ASCENDING)], unique=True),
    ]
    apply_indexes()
    check_indexes(["_id", "username"])


def test_add_indexes():
    TestIndexes.Config.indexes = [  # type: ignore
        IndexModel([("username", ASCENDING)], unique=True),
        IndexModel([("created_at", ASCENDING)], unique=True),
    ]
    apply_indexes()
    check_indexes(["_id", "username", "created_at"])


def test_remove_indexes():
    TestIndexes.Config.indexes = [  # type: ignore
        IndexModel([("created_at", ASCENDING)], unique=True),
    ]
    apply_indexes()
    check_indexes(["_id", "created_at"])


def test_indexes_for_all_db():
    from .models.course import Comment, ContentDescription, ContentImage, Course  # noqa
    from .models.user import User  # noqa

    apply_indexes()


def test_indexes_for_multiple_database():
    disconnect()  # first disconnect init_config connection

    class Log(Document):
        message: Optional[str] = None
        created_at: datetime = Field(default_factory=datetime.utcnow)

        class Config:
            database = "logging"
            indexes = [IndexModel([("created_at", ASCENDING)])]

    connect(DB_URL, databases=databases)
    Log(message="testing multiple database").create()

    apply_indexes()
