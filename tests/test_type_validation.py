import logging

from bson import ObjectId

from .conftest import init_config  # noqa
from mongodb_odm.types import PydanticObjectId

logger = logging.getLogger(__name__)


def test_validate_pydantic_object_id():
    obj = PydanticObjectId()
    assert isinstance(obj, ObjectId)

    obj = PydanticObjectId.validate(obj)
    assert isinstance(obj, ObjectId)

    obj = PydanticObjectId.validate(str(obj))
    assert isinstance(obj, ObjectId)

    try:
        _ = PydanticObjectId.validate("invalid-object-id")
        assert False
    except Exception as e:
        assert str(e) != "assert False"


def test_invalid_object_id():
    try:
        _ = PydanticObjectId.validate("invalid ObjectId")
        assert False
    except Exception as e:
        assert str(e) != "assert False"
