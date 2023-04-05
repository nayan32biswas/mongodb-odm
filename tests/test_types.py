from bson import ObjectId
from mongodb_odm import ODMObjectId


def test_odm_object_id():
    obj_id = ODMObjectId(ObjectId())

    assert isinstance(
        obj_id, ObjectId
    ), "ODMObjectId should be as same as ObjectId"


def test_odm_object_id_str():
    obj_id = ODMObjectId(str(ObjectId()))

    assert isinstance(
        obj_id, ObjectId
    ), "string ObjectId should convert to ObjectId"


def test_odm_object_id_error():
    try:
        # request with invalid data
        _ = ODMObjectId().validate(1)  # type: ignore
        assert False
    except Exception as e:
        assert str(e) != "assert False"
