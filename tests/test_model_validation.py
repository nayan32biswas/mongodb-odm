from typing import Optional

import pytest
from mongodb_odm import Document
from mongodb_odm.exceptions import InvalidConfiguration, ObjectDoesNotExist
from mongodb_odm.utils.validation import validate_filter_dict

from tests.conftest import INIT_CONFIG
from tests.models.course import ContentDescription, Course


@pytest.mark.usefixtures(INIT_CONFIG)
def test_document_as_model_error():
    with pytest.raises(InvalidConfiguration) as exc_info:
        _ = Document().create()

    assert type(exc_info.value) is InvalidConfiguration, (
        "The Document class should not be used as a model directly"
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_invalid_allow_inheritance():
    class Parent(Document):
        field: Optional[int] = None

    class Child(Parent):
        other_field: Optional[int] = None

    with pytest.raises(InvalidConfiguration) as exc_info:
        _ = Child().create()

    assert type(exc_info.value) is InvalidConfiguration, (
        "The parent should have ODMConfig with allow_inheritance=True"
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_allow_inheritance_true_for_child_and_parent():
    class Parent(Document):
        field: Optional[int] = None

        class ODMConfig(Document.ODMConfig):
            allow_inheritance = True

    class Child(Parent):
        other_field: Optional[int] = None

        class ODMConfig(Document.ODMConfig):
            allow_inheritance = True

    with pytest.raises(InvalidConfiguration) as exc_info:
        _ = Child().create()

    assert type(exc_info.value) is InvalidConfiguration, (
        "The child model has allow_inheritance=True. ODM does not allow multi level inheritance"
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_invalid_Config():
    class Parent(Document):
        field: Optional[int] = None

        class ODMConfig(Document.ODMConfig):
            collection_name = "course"
            allow_inheritance = False

    class Child(Parent):
        other_field: Optional[int] = None

    with pytest.raises(InvalidConfiguration) as exc_info:
        _ = Child().create()

    assert type(exc_info.value) is InvalidConfiguration, (
        "The parent model has allow_inheritance=False, so child model cannot be created"
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_get_error_on_null_obj():
    with pytest.raises(ObjectDoesNotExist) as exc_info:
        _ = Course.get({"_id": -1})

    assert type(exc_info.value) is ObjectDoesNotExist, (
        "Expected ObjectDoesNotExist for no documents found"
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_get_random_one_none():
    with pytest.raises(ObjectDoesNotExist) as exc_info:
        ContentDescription.get_random_one({"_id": -1})

    assert type(exc_info.value) is ObjectDoesNotExist, (
        "Expected ObjectDoesNotExist for no documents found"
    )


def test_validate_filter_dict_invalid_dotted_key():
    with pytest.raises(ValueError) as exc_info:
        validate_filter_dict(Course, {"nonexistent_field.some_nested": "value"})

    assert type(exc_info.value) is ValueError, (
        "Expected ValueError for invalid dotted key"
    )
