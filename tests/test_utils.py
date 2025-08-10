from typing import Optional, Union
from unittest.mock import Mock

import pytest
from mongodb_odm import Document, ODMObjectId, Relationship
from mongodb_odm.utils._internal_models import RelationalFieldInfo
from mongodb_odm.utils.utils import (
    _get_fields_info,
    _is_union_type,
    camel_to_snake,
    convert_model_to_collection,
    get_database_name,
    get_relationship_fields_info,
    get_type_from_field,
)
from pydantic import BaseModel, Field


class TestCamelToSnake:
    def test_camel_to_snake_simple(self):
        assert camel_to_snake("UserModel") == "user_model"
        assert camel_to_snake("Course") == "course"
        assert camel_to_snake("BlogPost") == "blog_post"

    def test_camel_to_snake_complex(self):
        assert camel_to_snake("HTTPRequest") == "h_t_t_p_request"
        assert camel_to_snake("XMLHttpRequest") == "x_m_l_http_request"

    def test_camel_to_snake_edge_cases(self):
        assert camel_to_snake("") == ""
        assert camel_to_snake("A") == "a"
        assert camel_to_snake("lowercase") == "lowercase"


class TestGetDatabaseName:
    def test_get_database_name_with_database(self):
        class MockModel:
            class ODMConfig:
                database = "test_db"

        result = get_database_name(MockModel)
        assert result == "test_db"

    def test_get_database_name_without_database(self):
        class MockModel:
            class ODMConfig:
                pass

        result = get_database_name(MockModel)
        assert result is None

    def test_get_database_name_no_config(self):
        class MockModel:
            pass

        # This would raise AttributeError in practice
        with pytest.raises(AttributeError):
            get_database_name(MockModel)


class TestConvertModelToCollection:
    def test_convert_model_to_collection_with_collection_name(self):
        class MockModel:
            class ODMConfig:
                collection_name = "custom_users"

        result = convert_model_to_collection(MockModel)
        assert result == "custom_users"

    def test_convert_model_to_collection_with_none_collection_name(self):
        class MockModel:
            class ODMConfig:
                collection_name = None

        result = convert_model_to_collection(MockModel)
        assert result == "mock_model"

    def test_convert_model_to_collection_no_config(self):
        class MockModel:
            pass

        # This would raise AttributeError in practice
        with pytest.raises(AttributeError):
            convert_model_to_collection(MockModel)


class TestIsUnionType:
    def test_is_union_type_with_union(self):
        assert _is_union_type(Union) is True

    def test_is_union_type_with_str(self):
        assert _is_union_type(str) is False

    def test_is_union_type_with_int(self):
        assert _is_union_type(int) is False


class TestGetTypeFromField:
    def test_get_type_from_field_simple_type(self):
        # Mock field with simple annotation
        mock_field = Mock()
        mock_field.annotation = str

        result = get_type_from_field(mock_field)
        assert result is str

    def test_get_type_from_field_none_annotation(self):
        mock_field = Mock()
        mock_field.annotation = None

        with pytest.raises(ValueError, match="Missing field type"):
            get_type_from_field(mock_field)

    def test_get_type_from_field_optional(self):
        mock_field = Mock()
        mock_field.annotation = Optional[str]

        result = get_type_from_field(mock_field)
        assert result is str

    def test_get_type_from_field_list(self):
        mock_field = Mock()
        mock_field.annotation = list[str]

        result = get_type_from_field(mock_field)
        assert result is str

    def test_get_type_from_field_invalid_union_too_many_args(self):
        mock_field = Mock()
        mock_field.annotation = Union[str, int, float]

        with pytest.raises(
            ValueError, match="Cannot have a \\(non-optional\\) union as a ODM field"
        ):
            get_type_from_field(mock_field)

    def test_get_type_from_field_invalid_union_no_none(self):
        mock_field = Mock()
        mock_field.annotation = Union[str, int]

        with pytest.raises(
            ValueError, match="Cannot have a \\(non-optional\\) union as a ODM field"
        ):
            get_type_from_field(mock_field)


class TestGetFieldsInfo:
    def test_get_fields_info_success(self):
        # Create a mock model class
        class User(BaseModel):
            id: str

        class MockModel(BaseModel):
            author_id: str = Field(...)
            author: Optional[User] = Relationship(local_field="author_id")

        result = _get_fields_info(MockModel, ["author"])

        assert len(result) == 1
        assert "author" in result
        assert isinstance(result["author"], RelationalFieldInfo)
        assert result["author"].model == User
        assert result["author"].local_field == "author_id"

    def test_get_fields_info_invalid_local_field(self):
        class User(Document):
            id: str

        class MockModel(BaseModel):
            author: Optional[User] = Relationship(local_field="nonexistent_field")

        with pytest.raises(
            Exception, match='Invalid field "nonexistent_field" in Relationship'
        ):
            _get_fields_info(MockModel, ["author"])


class TestGetRelationshipFieldsInfo:
    def test_get_relationship_fields_info_with_relationships(self):
        class User(Document):
            id: str

        class MockModel(Document):
            title: str = Field(...)
            author_id: ODMObjectId = Field(...)
            author: Optional[User] = Relationship(local_field="author_id")

        result = get_relationship_fields_info(MockModel)

        assert len(result) == 1
        assert "author" in result
        assert isinstance(result["author"], RelationalFieldInfo)

    def test_get_relationship_fields_info_no_relationships(self):
        class MockModel(BaseModel):
            title: str = Field(...)

        result = get_relationship_fields_info(MockModel)

        assert len(result) == 0
        assert result == {}
