import pytest
from bson import ObjectId
from mongodb_odm.types import ODMObjectId

from tests.conftest import INIT_CONFIG
from tests.models.course import Course


@pytest.mark.usefixtures(INIT_CONFIG)
def test_validate_pydantic_object_id():
    obj = ODMObjectId()
    assert isinstance(obj, ObjectId)

    obj = ODMObjectId(obj)
    assert isinstance(obj, ObjectId)

    obj = ODMObjectId(str(obj))
    assert isinstance(obj, ObjectId)

    try:
        _ = ODMObjectId.validate("invalid-object-id")
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


@pytest.mark.usefixtures(INIT_CONFIG)
def test_invalid_object_id():
    try:
        _ = ODMObjectId.validate("invalid ObjectId")
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


@pytest.mark.usefixtures(INIT_CONFIG)
def test_id_with__id():
    course = Course(author_id=ODMObjectId(), title="temp title").create()
    assert course.id == course._id, "id and _id should have same value"

    course.id = ODMObjectId()
    assert course.id == course._id, "id and _id should share same value"

    course._id = ODMObjectId()
    assert course.id == course._id, "id and _id should share same value"
