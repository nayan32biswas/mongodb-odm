from datetime import datetime
from typing import Any, List, Optional

import pytest
from mongodb_odm import (
    ASCENDING,
    TEXT,
    Document,
    Field,
    IndexModel,
    connect,
    disconnect,
)
from mongodb_odm.utils.apply_indexes import apply_indexes

from tests.conftest import INIT_CONFIG, MONGO_URL

databases = {"logging"}


class TestIndexes(Document):
    title: str = Field(max_length=255)
    slug: str = Field(...)
    short_description: Optional[str] = Field(max_length=512, default=None)
    created_at: datetime = Field(default_factory=datetime.now)

    class ODMConfig(Document.ODMConfig):
        collection_name = "test_indexes"
        indexes = [
            IndexModel([("slug", ASCENDING)], unique=True),
            IndexModel([("title", TEXT), ("short_description", TEXT)]),
        ]


@pytest.mark.usefixtures(INIT_CONFIG)
def test_create_indexes_without_connection():
    disconnect()

    try:
        apply_indexes()
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


@pytest.mark.usefixtures(INIT_CONFIG)
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
    assert AssertionError(), f"'{each_index_keys}' is invalid index"


def check_indexes(model: Any, index_keys: List[List[str]]):
    # fmt: off
    db_indexes = [index.to_dict() for index in model._get_collection().list_indexes()]
    # fmt: on
    assert len(index_keys) == len(db_indexes), "Number of indexes does not match"

    for each_index_keys in index_keys:
        check_each_index(db_indexes, each_index_keys)
    return True


@pytest.mark.usefixtures(INIT_CONFIG)
def test_indexes_create_add_update_remove():
    """
    Write a big testing function to test index initial create, add, update, and remove.
    If we implement separate tests for each functionality then the flow test remains incomplete.
    Because for each test we drop the database.
    """

    """Initially create all indexes"""
    TestIndexes.ODMConfig.indexes = [
        IndexModel([("slug", ASCENDING)], unique=True),
        IndexModel([("title", TEXT), ("short_description", TEXT)]),
    ]
    apply_indexes()
    check_indexes(TestIndexes, [["_id"], ["slug"], ["title", "short_description"]])

    """Add new indexes"""
    TestIndexes.ODMConfig.indexes = [
        IndexModel([("slug", ASCENDING)], unique=True),
        IndexModel([("created_at", ASCENDING)], unique=True),
        IndexModel([("title", TEXT), ("short_description", TEXT)]),
    ]
    apply_indexes()
    check_indexes(
        TestIndexes, [["_id"], ["slug"], ["created_at"], ["title", "short_description"]]
    )

    """Update existing indexes values"""
    TestIndexes.ODMConfig.indexes = [
        IndexModel([("slug", ASCENDING)], unique=True),
        IndexModel([("created_at", ASCENDING)]),
        IndexModel(
            [("title", TEXT), ("short_description", TEXT)], default_language="english"
        ),
    ]
    apply_indexes()
    check_indexes(
        TestIndexes, [["_id"], ["created_at"], ["slug"], ["title", "short_description"]]
    )

    """Remove some of indexes"""
    TestIndexes.ODMConfig.indexes = [
        IndexModel([("created_at", ASCENDING)], unique=True),
    ]
    apply_indexes()
    check_indexes(TestIndexes, [["_id"], ["created_at"]])

    """No index was changed"""
    TestIndexes.ODMConfig.indexes = [
        IndexModel([("created_at", ASCENDING)], unique=True),
    ]
    apply_indexes()
    check_indexes(TestIndexes, [["_id"], ["created_at"]])


@pytest.mark.usefixtures(INIT_CONFIG)
def test_text_indexes():
    """Make sure text index created properly"""

    TestIndexes.ODMConfig.indexes = [
        IndexModel([("slug", ASCENDING)], unique=True),
    ]
    apply_indexes()
    check_indexes(TestIndexes, [["_id"], ["slug"]])

    TestIndexes.ODMConfig.indexes = [
        IndexModel([("slug", ASCENDING)], unique=True),
        IndexModel([("title", TEXT)]),
    ]
    apply_indexes()
    check_indexes(TestIndexes, [["_id"], ["slug"], ["title"]])


@pytest.mark.usefixtures(INIT_CONFIG)
def test_text_filter():
    TestIndexes.ODMConfig.indexes = [
        IndexModel([("slug", ASCENDING)], unique=True),
        IndexModel([("title", TEXT), ("short_description", TEXT)]),
    ]
    apply_indexes()
    text_data = TestIndexes(
        title="How to connection Mongodb in Mongodb-ODM", slug="one"
    ).create()
    text_data = TestIndexes.find_one(filter={"$text": {"$search": "mongodb"}})
    assert text_data is not None


@pytest.mark.usefixtures(INIT_CONFIG)
def test_child_indexes_only():
    class ParentModel(Document):
        title: str = Field(...)

        class ODMConfig(Document.ODMConfig):
            allow_inheritance = True

    class ChildModel(ParentModel):
        child_title: str = Field(...)

        class ODMConfig(Document.ODMConfig):
            indexes = [
                IndexModel([("child_title", ASCENDING)]),
            ]

    apply_indexes()
    check_indexes(ParentModel, [["_id"], ["_cls"], ["child_title"]])


@pytest.mark.usefixtures(INIT_CONFIG)
def test_child_indexes_without_cls_index():
    class ParentModel(Document):
        title: str = Field(...)

        class ODMConfig(Document.ODMConfig):
            allow_inheritance = True
            index_inheritance_field = False

    class ChildModel(ParentModel):
        child_title: str = Field(...)

        class ODMConfig(Document.ODMConfig):
            indexes = [
                IndexModel([("child_title", ASCENDING)]),
            ]

    apply_indexes()
    check_indexes(ParentModel, [["_id"], ["child_title"]])


@pytest.mark.usefixtures(INIT_CONFIG)
def test_indexes_for_all_db():
    from tests.models.course import ContentDescription  # noqa
    from tests.models.course import Comment, ContentImage, Course  # noqa
    from tests.models.user import User  # noqa

    apply_indexes()


@pytest.mark.usefixtures(INIT_CONFIG)
def test_indexes_for_multiple_database():
    disconnect()  # first disconnect init_config connection

    class Log(Document):
        message: Optional[str] = None
        created_at: datetime = Field(default_factory=datetime.now)

        class ODMConfig:
            database = "logging"
            indexes = [IndexModel([("created_at", ASCENDING)])]

    connect(MONGO_URL, databases=databases)
    Log(message="testing multiple database").create()

    apply_indexes()

    Log.ODMConfig.database = None  # type: ignore
