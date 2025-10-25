from collections.abc import Mapping, Sequence
from typing import Any, TypeVar, Union

from bson import ObjectId
from pydantic import GetCoreSchemaHandler
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
DICT_TYPE = dict[str, Any]
SORT_TYPE = Union[str, Sequence[tuple[str, Union[int, str, Mapping[str, Any]]]]]

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
    _example_object_id = str(ObjectId())

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, handler: GetCoreSchemaHandler
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
                lambda x: str(x),  # Always serialize as string
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def validate(cls, v: Union[str, ObjectId]) -> str:
        if isinstance(v, ObjectId):
            return cls(str(v))
        elif isinstance(v, str):
            try:
                return cls(str(ObjectId(v)))
            except Exception as e:
                raise ValueError("Invalid ObjectId") from e

        raise ValueError("Invalid data. ObjectId required")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> Any:
        """Provide OpenAPI/JSON Schema metadata."""
        json_schema: Any = handler(schema)
        json_schema.update(
            type="string",
            format="objectid",
            example=cls._example_object_id,
        )
        return json_schema
