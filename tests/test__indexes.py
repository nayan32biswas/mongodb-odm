import logging
from datetime import datetime
from typing import List, Optional

from pymongo import TEXT

from mongodb_odm import ASCENDING, Document, Field, IndexModel, connect, disconnect
from mongodb_odm.utils.apply_indexes import apply_indexes

from .conftest import DB_URL, init_config  # noqa

databases = {"logging"}
logger = logging.getLogger(__name__)


class TestIndexes(Document):
    username: str = Field(...)
    title: str = Field(max_length=255)
    short_description: Optional[str] = Field(max_length=512, default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config(Document.Config):
        collection_name = "test_indexes"
        indexes = [
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel([("title", TEXT), ("short_description", TEXT)]),
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


def check_each_index(db_indexes, each_index_keys):
    for db_index in db_indexes:
        is_match = True
        for index_key in each_index_keys:
            """Check if all item is available in single db-index key"""
            if index_key in db_index["key"] or index_key in db_index.get("weights", {}):
                continue
            is_match = False
            break
        if is_match:
            return True
    assert False, f"'{each_index_keys}' is invalid index"


def check_indexes(index_keys: List[List[str]]):
    db_indexes = [index.to_dict() for index in TestIndexes._get_collection().list_indexes()]  # type: ignore
    assert len(index_keys) == len(db_indexes), "Number of indexes does not match"

    for each_index_keys in index_keys:
        check_each_index(db_indexes, each_index_keys)
    return True


def test_indexes_create_add_update_remove():
    """
    Write a big testing function to test index initial create, add, update, and remove.
    If we implement separate tests for each functionality then the flow test remains incomplete.
    Because for each test we drop the database.
    """

    """Initially create all indexes"""
    TestIndexes.Config.indexes = [
        IndexModel([("username", ASCENDING)], unique=True),
        IndexModel([("title", TEXT), ("short_description", TEXT)]),
    ]
    apply_indexes()
    check_indexes([["_id"], ["username"], ["title", "short_description"]])

    """Add new indexes"""
    TestIndexes.Config.indexes = [
        IndexModel([("username", ASCENDING)], unique=True),
        IndexModel([("created_at", ASCENDING)], unique=True),
        IndexModel([("title", TEXT), ("short_description", TEXT)]),
    ]
    apply_indexes()
    check_indexes(
        [["_id"], ["username"], ["created_at"], ["title", "short_description"]]
    )

    """Update existing indexes values"""
    TestIndexes.Config.indexes = [
        IndexModel([("username", ASCENDING)], unique=True),
        IndexModel([("created_at", ASCENDING)]),
        IndexModel(
            [("title", TEXT), ("short_description", TEXT)], default_language="english"
        ),
    ]
    apply_indexes()
    check_indexes(
        [["_id"], ["created_at"], ["username"], ["title", "short_description"]]
    )

    """Remove some of indexes"""
    TestIndexes.Config.indexes = [
        IndexModel([("created_at", ASCENDING)], unique=True),
    ]
    apply_indexes()
    check_indexes([["_id"], ["created_at"]])

    """No index was changed"""
    TestIndexes.Config.indexes = [
        IndexModel([("created_at", ASCENDING)], unique=True),
    ]
    apply_indexes()
    check_indexes([["_id"], ["created_at"]])


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
