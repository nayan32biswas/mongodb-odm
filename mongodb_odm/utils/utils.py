import re
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel

from ..fields import _RelationshipInfo
from ._internal_models import RelationalFieldInfo

pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(string: str) -> str:
    return pattern.sub("_", string).lower()


def get_database_name(model: Any) -> Optional[Any]:
    """
    Get the database name if the model Config has a user-defined database name.

    model: Document type
    """
    if hasattr(model.Config, "database"):
        return model.Config.database
    return None


def convert_model_to_collection(model: Any) -> str:
    """
    Get the collection name from the model.
    Users could define collection names in model Config.
    Otherwise, we will convert the model name to a snake case collection name.

    The user defines collection_name as a higher priority here.

    model: Document type
    """
    if (
        hasattr(model.Config, "collection_name")
        and model.Config.collection_name is not None
    ):
        """By default model has Config in BaseModel"""
        return str(model.Config.collection_name)
    else:
        return camel_to_snake(model.__name__)


def _get_fields_info(
    cls: Type[BaseModel], fields: List[str]
) -> Dict[str, RelationalFieldInfo]:
    """
    Extract related field information for a model for specific fields.
    """
    field_data: Dict[str, RelationalFieldInfo] = {}
    for field in fields:
        obj = cls.__fields__[field]
        if obj.default.local_field not in cls.__fields__:
            # Check Relationship local_field exists in the model
            raise Exception(
                f'Invalid field "{obj.default.local_field}" in Relationship'
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
        field_data[field] = RelationalFieldInfo(
            model=obj.type_,  # User
            local_field=obj.default.local_field,  # author_id
            related_field=obj.default.related_field,  # author
        )
    return field_data


def get_relationship_fields_info(
    cls: Type[BaseModel],
) -> Dict[str, RelationalFieldInfo]:
    """
    This function will return all of the related fields with their information.

    cls: Document
    """
    fields_name = []
    for field_name, field_info in cls.__fields__.items():
        """Get all fields that are related to a specific model."""
        if type(field_info.default) is _RelationshipInfo:
            fields_name.append(field_name)
    return _get_fields_info(cls, fields_name)
