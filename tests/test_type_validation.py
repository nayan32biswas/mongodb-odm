import logging

from bson import ObjectId
from mongodb_odm.types import ODMObjectId

from .conftest import init_config  # noqa

logger = logging.getLogger(__name__)


def test_validate_pydantic_object_id():
    obj = ODMObjectId()
    assert isinstance(obj, ObjectId)

    obj = ODMObjectId.validate(obj)
    assert isinstance(obj, ObjectId)

    obj = ODMObjectId.validate(str(obj))
    assert isinstance(obj, ObjectId)

    try:
        _ = ODMObjectId.validate("invalid-object-id")
        assert False
    except Exception as e:
        assert str(e) != "assert False"


def test_invalid_object_id():
    try:
        _ = ODMObjectId.validate("invalid ObjectId")
        assert False
    except Exception as e:
        assert str(e) != "assert False"
