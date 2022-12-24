from datetime import datetime
import logging
from typing import List
from pydantic import Field
from pymongo import IndexModel, ASCENDING

from mongodb_odm.apply_indexes import apply_indexes
from mongodb_odm import Document
from .conftest import init_config  # noqa


logger = logging.getLogger(__name__)


class TestIndexes(Document):
    username: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "test_indexes"
        indexes = [
            IndexModel([("username", ASCENDING)], unique=True),
        ]


def check_indexes(index_keys: List[str]):
    for i, index in enumerate(TestIndexes._get_collection().list_indexes()):
        print(i, index)
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
    from .models.comment import Comment  # noqa
    from .models.post import Post, ContentDescription, ContentImage  # noqa
    from .models.user import User  # noqa

    apply_indexes()
