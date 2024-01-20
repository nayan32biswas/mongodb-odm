from typing import Annotated, Any, Dict, Mapping, Sequence, Tuple, Union

from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

# Common types
DICT_TYPE = Dict[str, Any]
SORT_TYPE = Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]]


class _ODMObjectIdAnnotation:
    """
    Since ObjectId has not validation and raise error as pydantic type
    we extend ObjectId for type support.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, _handler
    ) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            """No conversion needed if type are already ObjectId"""
            return v
        try:
            """
            If value is valid string for ObjectId then convert it ObjectId
            or it will raise error from ObjectId validation
            """
            s = handler(v)
            return ObjectId(s)
        except Exception as e:
            raise ValueError("Invalid data. ObjectId required") from e


ODMObjectId = Annotated[ObjectId, _ODMObjectIdAnnotation]
