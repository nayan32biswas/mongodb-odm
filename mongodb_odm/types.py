from typing import Any, Dict, Mapping, Sequence, Tuple, Union

from bson import ObjectId

# Common types
DICT_TYPE = Dict[str, Any]
SORT_TYPE = Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]]


class ODMObjectId(ObjectId):
    """
    Since ObjectId has not validation and raise error as pydantic type
    we extend ObjectId for type support.
    """

    @classmethod
    def __get_validators__(cls: Any) -> Any:
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, ObjectId]) -> ObjectId:
        if isinstance(v, ObjectId):
            """No conversion needed if type are already ObjectId"""
            return v
        elif isinstance(v, str):
            """
            If value is valid string for ObjectId then convert it ObjectId
            or it will raise error from ObjectId validation
            """
            return ObjectId(v)
        raise TypeError("Invalid data. ObjectId required")
