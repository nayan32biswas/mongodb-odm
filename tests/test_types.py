from bson import ObjectId

from mongodb_odm import PydanticObjectId


def test_pydantic_object_id():
    obj_id = PydanticObjectId(ObjectId())

    assert isinstance(obj_id, ObjectId), "PydanticObjectId should be as same as ObjectId"


def test_pydantic_object_id_str():
    obj_id = PydanticObjectId(str(ObjectId()))

    assert isinstance(obj_id, ObjectId), "string ObjectId should convert to ObjectId"
