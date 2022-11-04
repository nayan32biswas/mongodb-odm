import os
from typing import List
import pytest
from datetime import datetime
from pydantic import Field
from pymongo import IndexModel, ASCENDING

from ..apply_indexes import apply_indexes
from ..models import Document
from ..connection import connect

DB_URL = os.environ.get(
    "TEST_MONGO_HOST", "mongodb://root:password@db:27017/test?authSource=admin"
)


@pytest.fixture(autouse=True)
def init_config():
    print("Initiate database")

    connect(DB_URL)

    yield None

    # disconnect()
    print("Clean everything")


class IndexesTestDocument(Document):
    username: str
    title: str

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "indexes_test_document"
        indexes = (IndexModel([("username", ASCENDING)], unique=True),)


def check_indexes(index_keys: List[str]):
    for i, index in enumerate(IndexesTestDocument._get_collection().list_indexes()):
        assert index_keys[i] in index.to_dict()["key"]
    return True


def test_create_indexes():
    apply_indexes()

    check_indexes(["_id", "username"])


def test_add_indexes():
    IndexesTestDocument.Config.indexes = (  # type: ignore
        IndexModel([("username", ASCENDING)], unique=True),
        IndexModel([("created_at", ASCENDING)], unique=True),
    )
    apply_indexes()
    check_indexes(["_id", "username", "created_at"])


def test_remove_indexes():
    IndexesTestDocument.Config.indexes = (
        IndexModel([("created_at", ASCENDING)], unique=True),
    )
    apply_indexes()
    check_indexes(["_id", "created_at"])
