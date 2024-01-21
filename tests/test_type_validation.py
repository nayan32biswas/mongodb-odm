import logging

from bson import ObjectId
from mongodb_odm.types import ODMObjectId

from .conftest import init_config  # noqa

logger = logging.getLogger(__name__)


def test_validate_pydantic_object_id():
    obj = ODMObjectId()
    assert isinstance(obj, ObjectId)

    obj = ODMObjectId(obj)
    assert isinstance(obj, ObjectId)

    obj = ODMObjectId(str(obj))
    assert isinstance(obj, ObjectId)

    try:
        _ = ODMObjectId("invalid-object-id")
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_invalid_object_id():
    try:
        _ = ODMObjectId("invalid ObjectId")
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""
