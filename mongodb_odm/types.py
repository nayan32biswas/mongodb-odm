from collections.abc import Mapping, Sequence
from typing import Any, Dict, Tuple, TypeVar, Union

from bson import ObjectId
from pydantic_core import core_schema
from pymongo.operations import (
    DeleteMany,
    DeleteOne,
    InsertOne,
    ReplaceOne,
    UpdateMany,
    UpdateOne,
)

# Common types
DICT_TYPE = Dict[str, Any]
SORT_TYPE = Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]]

DocumentType = TypeVar("DocumentType", bound=Mapping[str, Any])

WriteOp = Union[
    InsertOne[DocumentType],
    DeleteOne,
    DeleteMany,
    ReplaceOne[DocumentType],
    UpdateOne,
    UpdateMany,
]


class ODMObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.chain_schema(
                [
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]
            ),
            python_schema=core_schema.chain_schema(
                [
                    core_schema.union_schema(
                        [
                            core_schema.is_instance_schema(ObjectId),
                            core_schema.str_schema(),
                        ]
                    ),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: ObjectId(x)
            ),
        )

    @classmethod
    def validate(cls, v: Union[str, ObjectId]) -> ObjectId:
        if isinstance(v, ObjectId):
            """No conversion needed if type are already ObjectId"""
            return v
        try:
            return ObjectId(v)
        except Exception as e:
            raise ValueError("Invalid data. ObjectId required") from e


class ObjectIdStr(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.chain_schema(
                [
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]
            ),
            python_schema=core_schema.chain_schema(
                [
                    core_schema.union_schema(
                        [
                            core_schema.is_instance_schema(ObjectId),
                            core_schema.str_schema(),
                        ]
                    ),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v: Union[str, ObjectId]) -> str:
        if isinstance(v, ObjectId):
            return str(v)
        elif isinstance(v, str):
            try:
                return str(ObjectId(v))
            except Exception as e:
                raise ValueError("Invalid ObjectId") from e

        raise ValueError("Invalid data. ObjectId required")
