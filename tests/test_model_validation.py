import logging

from mongodb_odm import Document
from typing import Optional

from .conftest import init_config  # noqa
from .models.post import Post, ContentDescription

logger = logging.getLogger(__name__)


def test_document_as_model_error():
    try:
        _ = Document().create()
        assert False
    except Exception as e:
        assert str(e) != "assert False"


def test_invalid_allow_inheritance():
    class Parent(Document):
        field: Optional[int] = None

    class Child(Parent):
        other_field: Optional[int] = None

    try:
        _ = Child().create()
        assert False
    except Exception as e:
        assert str(e) != "assert False"


def test_invalid_Config():
    class Parent(Document):
        field: Optional[int] = None

        class Config:
            collection_name = "post"
            allow_inheritance = False

    class Child(Parent):
        other_field: Optional[int] = None

    try:
        _ = Child().create()
        assert False
    except Exception as e:
        assert str(e) != "assert False"


def test_get_error_on_null_obj():
    try:
        _ = Post.get({"_id": -1})
        assert False
    except Exception as e:
        assert str(e) != "assert False"


def test_get_random_one_none():
    obj = ContentDescription.get_random_one({"_id": -1})
    assert obj is None
