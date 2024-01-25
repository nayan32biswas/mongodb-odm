import logging
from typing import Optional

from mongodb_odm import Document

from .conftest import init_config  # noqa
from .models.course import ContentDescription, Course
from .utils import populate_data

logger = logging.getLogger(__name__)


def test_document_as_model_error():
    try:
        _ = Document().create()
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_invalid_allow_inheritance():
    class Parent(Document):
        field: Optional[int] = None

    class Child(Parent):
        other_field: Optional[int] = None

    try:
        _ = Child().create()
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_allow_inheritance_true_for_child_and_parent():
    class Parent(Document):
        field: Optional[int] = None

        class ODMConfig(Document.ODMConfig):
            allow_inheritance = True

    class Child(Parent):
        other_field: Optional[int] = None

        class ODMConfig(Document.ODMConfig):
            allow_inheritance = True

    try:
        _ = Child().create()
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_invalid_Config():
    class Parent(Document):
        field: Optional[int] = None

        class ODMConfig(Document.ODMConfig):
            collection_name = "course"
            allow_inheritance = False

    class Child(Parent):
        other_field: Optional[int] = None

    try:
        _ = Child().create()
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_get_error_on_null_obj():
    populate_data()
    try:
        _ = Course.get({"_id": -1})
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_get_random_one_none():
    try:
        _ = ContentDescription.get_random_one({"_id": -1})
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""
