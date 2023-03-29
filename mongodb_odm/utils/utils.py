import re
from typing import Any, List

from ..fields import _RelationshipInfo

pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(string: str) -> str:
    return pattern.sub("_", string).lower()


def convert_model_to_collection(model: Any) -> str:
    if (
        hasattr(model.Config, "collection_name")
        and model.Config.collection_name is not None
    ):
        """By default model has Config in BaseModel"""
        return model.Config.collection_name
    else:
        return camel_to_snake(model.__name__)


def _get_fields_info(cls, fields: List[str]):
    field_data = {}
    for field in fields:
        obj = cls.__fields__[field]
        if obj.default.local_field not in cls.__fields__:
            raise Exception(
                f'Invalid field "{obj.default.local_field}" in Relationship'
            )
        field_data[field] = {
            "model": obj.type_,
            "local_field": obj.default.local_field,
            "related_field": obj.default.related_field,
        }
    return field_data


def get_relationship_fields_info(cls):
    fields_name = []
    for field_name, field_info in cls.__fields__.items():
        if type(field_info.default) == _RelationshipInfo:
            fields_name.append(field_name)
    return _get_fields_info(cls, fields_name)
