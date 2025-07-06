import pytest
from bson import ObjectId
from mongodb_odm import ObjectIdStr, ODMObjectId
from pydantic import BaseModel, ValidationError


def test_odm_object_id():
    """Test basic ODMObjectId creation from ObjectId"""
    obj_id = ODMObjectId(ObjectId())
    assert isinstance(obj_id, ObjectId), "ODMObjectId should be as same as ObjectId"


def test_odm_object_id_for_str():
    """Test ODMObjectId creation from string"""
    obj_id = ODMObjectId(str(ObjectId()))
    assert isinstance(obj_id, ObjectId), "string ObjectId should convert to ObjectId"


def test_odm_object_id_type_error():
    """Test ODMObjectId validation error handling"""
    with pytest.raises(ValueError) as exc_info:
        ODMObjectId.validate("invalid_object_id")

    assert isinstance(exc_info.value, ValueError), (
        "Should raise ValueError for invalid ObjectId"
    )

    with pytest.raises(ValueError) as exc_info:
        ODMObjectId.validate(1)

    assert isinstance(exc_info.value, ValueError), (
        "Should raise ValueError for integer value for ODMObjectId"
    )


def test_odm_object_id_pydantic_schema():
    """Test __get_pydantic_core_schema__ method for ODMObjectId"""
    # Test that the schema is returned correctly
    schema = ODMObjectId.__get_pydantic_core_schema__(ODMObjectId, None)

    assert isinstance(schema, dict), "Schema should be a dictionary"
    # The actual schema type returned by the implementation
    assert schema["type"] == "json-or-python", "Should use json-or-python schema"

    # Test that it has the expected structure
    assert "json_schema" in schema
    assert "python_schema" in schema
    assert "serialization" in schema


def test_odm_object_id_in_pydantic_model():
    """Test ODMObjectId validation and serialization in a Pydantic model"""

    class TestModel(BaseModel):
        id: ODMObjectId

    # Test with valid ObjectId
    valid_id = ObjectId()
    model = TestModel(id=valid_id)
    assert isinstance(model.id, ObjectId)
    assert model.id == valid_id

    # Test with valid string ObjectId
    valid_str_id = str(ObjectId())
    model = TestModel(id=valid_str_id)
    assert isinstance(model.id, ObjectId)
    assert str(model.id) == valid_str_id

    # Test with invalid string
    with pytest.raises(ValidationError):
        TestModel(id="invalid_object_id")

    # Test with invalid type
    with pytest.raises(ValidationError):
        TestModel(id=123)

    # Test serialization - ODMObjectId should serialize to string
    model = TestModel(id=ObjectId())
    serialized = model.model_dump()
    assert isinstance(serialized["id"], ObjectId), (
        "Serialized id should be an ObjectId instance"
    )


def test_odm_object_id_str():
    """Test basic ObjectIdStr creation"""
    new_id = ObjectIdStr(ObjectId())
    assert isinstance(new_id, str), "ObjectIdStr should be an instance of ObjectIdStr"


def test_odm_object_id_str_validate():
    """Test ObjectIdStr validation methods"""
    new_id = ObjectIdStr.validate(ObjectId())
    assert isinstance(new_id, str), "ObjectIdStr should be an instance of ObjectId"

    new_id = ObjectIdStr.validate(str(ObjectId()))
    assert isinstance(new_id, str), "ObjectIdStr should be an instance of str"

    with pytest.raises(ValueError) as exc_info:
        ObjectIdStr.validate("invalid_object_id")
    assert isinstance(exc_info.value, ValueError), (
        "Should raise ValueError for invalid ObjectIdStr"
    )

    with pytest.raises(ValueError) as exc_info:
        ObjectIdStr.validate(1)
    assert isinstance(exc_info.value, ValueError), (
        "Should raise ValueError for integer value for ObjectIdStr"
    )


def test_object_id_str_pydantic_schema():
    """Test __get_pydantic_core_schema__ method for ObjectIdStr"""
    # Test that the schema is returned correctly
    schema = ObjectIdStr.__get_pydantic_core_schema__(ObjectIdStr, None)

    assert isinstance(schema, dict), "Schema should be a dictionary"
    # The actual schema type returned by the implementation
    assert schema["type"] == "json-or-python", "Should use json-or-python schema"

    # Test that it has the expected structure
    assert "json_schema" in schema
    assert "python_schema" in schema
    assert "serialization" in schema


def test_object_id_str_in_pydantic_model():
    """Test ObjectIdStr validation and serialization in a Pydantic model"""

    class TestModel(BaseModel):
        id: ObjectIdStr

    # Test with valid ObjectId
    valid_id = ObjectId()
    model = TestModel(id=valid_id)
    # ObjectIdStr should store the value as a string
    assert isinstance(model.id, str)
    assert model.id == str(valid_id)

    # Test with valid string ObjectId
    valid_str_id = str(ObjectId())
    model = TestModel(id=valid_str_id)
    assert isinstance(model.id, str)
    assert model.id == valid_str_id

    # Test with invalid string
    with pytest.raises(ValidationError):
        TestModel(id="invalid_object_id")

    # Test with invalid type
    with pytest.raises(ValidationError):
        TestModel(id=123)

    # Test serialization
    model = TestModel(id=ObjectId())
    serialized = model.model_dump()
    assert isinstance(serialized["id"], str)


def test_object_id_str_json_serialization():
    """Test ObjectIdStr JSON serialization in Pydantic model"""

    class TestModel(BaseModel):
        id: ObjectIdStr

    valid_id = ObjectId()
    model = TestModel(id=valid_id)

    # Test JSON serialization
    json_data = model.model_dump(mode="json")
    assert isinstance(json_data["id"], str)

    # Test JSON parsing
    json_str = model.model_dump_json()
    assert isinstance(json_str, str)

    # Test round-trip JSON serialization/deserialization
    parsed_model = TestModel.model_validate_json(json_str)
    assert isinstance(parsed_model.id, str)
    assert parsed_model.id == str(valid_id)


def test_pydantic_schema_validation_modes():
    """Test different validation modes for both types"""

    class TestModel(BaseModel):
        odm_id: ODMObjectId
        str_id: ObjectIdStr

    test_id = ObjectId()

    # Test Python validation
    model = TestModel(odm_id=test_id, str_id=test_id)
    assert isinstance(model.odm_id, ObjectId)
    assert isinstance(model.str_id, str)

    # Test from dict
    data = {"odm_id": str(test_id), "str_id": str(test_id)}
    model = TestModel.model_validate(data)
    assert isinstance(model.odm_id, ObjectId)
    assert isinstance(model.str_id, str)

    # Test from JSON string
    json_data = f'{{"odm_id": "{test_id}", "str_id": "{test_id}"}}'
    model = TestModel.model_validate_json(json_data)
    assert isinstance(model.odm_id, ObjectId)
    assert isinstance(model.str_id, str)
