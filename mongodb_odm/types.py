from typing import Any, Dict, Mapping, Sequence, Tuple, Union

from bson import ObjectId

SORT_TYPE = Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]]

DICT_TYPE = Dict[str, Any]


class ODMObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls: Any) -> Any:
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, ObjectId]) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        elif isinstance(v, str):
            return ObjectId(v)
        raise TypeError("Invalid data. ObjectId required")
