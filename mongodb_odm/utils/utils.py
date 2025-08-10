import re
import types
from typing import Any, Optional, Union

from mongodb_odm.fields import RelationshipInfo
from mongodb_odm.utils._internal_models import RelationalFieldInfo
from pydantic import BaseModel
from typing_extensions import get_args, get_origin

UnionType = getattr(types, "UnionType", Union)
NoneType = type(None)
pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(string: str) -> str:
    return pattern.sub("_", string).lower()


def get_database_name(model: Any) -> Optional[Any]:
    """
    Get the database name if the model ODMConfig has a user-defined database name.

    model: Document type
    """
    if hasattr(model.ODMConfig, "database"):
        return model.ODMConfig.database

    return None


def convert_model_to_collection(model: Any) -> str:
    """
    Get the collection name from the model.
    Users could define collection names in model ODMConfig.
    Otherwise, we will convert the model name to a snake case collection name.

    The user defines collection_name as a higher priority here.

    model: Document type
    """
    if (
        hasattr(model.ODMConfig, "collection_name")
        and model.ODMConfig.collection_name is not None
    ):
        """By default model has ODMConfig in BaseModel"""
        return str(model.ODMConfig.collection_name)
    else:
        return camel_to_snake(model.__name__)


def _is_union_type(t: Any) -> bool:
    return t is UnionType or t is Union


def get_type_from_field(field: Any) -> Any:
    type_: Any = field.annotation

    # Resolve Optional fields
    if type_ is None:
        raise ValueError("Missing field type")

    origin = get_origin(type_)

    if origin is None:
        return type_

    if _is_union_type(origin):
        bases = get_args(type_)

        if len(bases) > 2:
            raise ValueError("Cannot have a (non-optional) union as a ODM field")
        # Non optional unions are not allowed
        if bases[0] is not NoneType and bases[1] is not NoneType:
            raise ValueError("Cannot have a (non-optional) union as a ODM field")

        # Optional unions are allowed
        return bases[0] if bases[0] is not NoneType else bases[1]
    elif origin is list:
        inner_type_ = get_args(type_)[0]
        return inner_type_

    return origin


def get_model_fields(cls: type[BaseModel]) -> dict[str, Any]:
    return cls.__pydantic_fields__


def _get_fields_info(
    cls: type[BaseModel], fields: list[str]
) -> dict[str, RelationalFieldInfo]:
    """
    Extract related field information for a model for specific fields.
    """
    field_data: dict[str, RelationalFieldInfo] = {}
    for field in fields:
        field_type_obj = get_model_fields(cls)[field]
        if field_type_obj.default.local_field not in get_model_fields(cls):
            # Check Relationship local_field exists in the model
            raise Exception(
                f'Invalid field "{field_type_obj.default.local_field}" in Relationship'
            )
        """
        Example relationship
        class User(Document):
            ...

        class Course(Document):
            ...
            author_id: ODMObjectId = Field(...)
            author: Optional[User] = Relationship(local_field="author_id")
        """
        field_type = get_type_from_field(field_type_obj)
        field_data[field] = RelationalFieldInfo(
            model=field_type,  # User
            local_field=field_type_obj.default.local_field,  # author_id
            related_field=field_type_obj.default.related_field,  # author
        )

    return field_data


def get_relationship_fields_info(
    cls: type[BaseModel],
) -> dict[str, RelationalFieldInfo]:
    """
    This function will return all of the related fields with their information.

    cls: Document
    """
    fields_name = []
    for field_name, field_info in get_model_fields(cls).items():
        """Get all fields that are related to a specific model."""
        if type(field_info.default) is RelationshipInfo:
            fields_name.append(field_name)

    return _get_fields_info(cls, fields_name)
