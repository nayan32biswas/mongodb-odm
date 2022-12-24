from datetime import datetime
from typing import Any, Iterator, List, Optional, Tuple
from typing_extensions import Self
from bson import ObjectId


from pydantic import BaseModel, Field
from pymongo import DESCENDING
from pymongo.cursor import Cursor
from pymongo.command_cursor import CommandCursor
from pymongo.results import UpdateResult, DeleteResult
from pymongo.collection import Collection

from .types import PydanticObjectId  # type: ignore
from .utils import convert_model_to_collection
from .connection import get_db, get_client


INHERITANCE_FIELD_NAME = "_cls"


class _BaseDocument(BaseModel):
    class Config:
        # Those fields will work as the default value of any child class.
        orm_mode = True
        allow_population_by_field_name = True
        collection_name = None
        allow_inheritance = False

    def __init__(self, *args, **kwargs) -> None:
        if type(self) is Document:
            raise Exception(
                "Document is an abstract class and cannot be instantiated directly"
            )
        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value) -> None:
        """Add '# type: ignore' as a comment if get type error while getting this value"""
        self.__dict__[key] = value

    @classmethod
    def _get_collection_class(cls) -> Any:
        model: Any = cls
        if model.__base__ != Document:
            base_model = model.__base__
            if (
                not hasattr(base_model.Config, "allow_inheritance")
                or base_model.Config.allow_inheritance is not True
            ):
                raise Exception(
                    f"Invalid model inheritance. {base_model} does not allow model inheritance."
                )
            return base_model, model
        else:
            return model, None

    @classmethod
    def _get_collection_name(cls) -> str:
        collection, _ = cls._get_collection_class()
        return convert_model_to_collection(collection)

    @classmethod
    def _get_child(cls) -> Optional[str]:
        _, collection = cls._get_collection_class()
        if collection is None:
            return None
        return convert_model_to_collection(collection)

    @classmethod
    def _get_collection(cls) -> Collection:
        if not hasattr(cls, "_collection") or cls._collection is None:
            db = get_db()
            cls._collection = db[cls._get_collection_name()]
        return cls._collection

    @classmethod
    def _db(cls) -> str:
        return cls._get_collection_name()

    @classmethod
    def start_session(cls):
        return get_client().start_session()


class Document(_BaseDocument):
    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")

    def create(self, get_obj=False, **kwargs) -> Self:
        _collection = self._get_collection()

        data = self.dict(exclude={"id"})
        if self._get_child() is not None:
            data = {f"{INHERITANCE_FIELD_NAME}": self._get_child(), **data}

        inserted_id = _collection.insert_one(data, **kwargs).inserted_id
        self.__dict__.update({"id": inserted_id})
        return self

    @classmethod
    def find_raw(cls, filter: dict = {}, projection: dict = {}, **kwargs) -> Cursor:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {f"{INHERITANCE_FIELD_NAME}": cls._get_child(), **filter}
        if projection:
            return _collection.find(filter, projection, **kwargs)
        return _collection.find(filter, **kwargs)

    @classmethod
    def find(
        cls,
        filter: dict = {},
        sort: Optional[List[Tuple[str, int]]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs,
    ) -> Iterator[Self]:
        qs = cls.find_raw(filter, **kwargs)
        if sort:
            qs = qs.sort(sort)
        if skip:
            qs = qs.skip(skip)
        if limit:
            qs = qs.limit(limit)

        model_childs = {}
        is_dynamic_model = False
        if (
            hasattr(cls.Config, "allow_inheritance")
            and cls.Config.allow_inheritance is True
        ):
            is_dynamic_model = True
            for model in cls.__subclasses__():
                model_childs[cls._get_child()] = model

        for data in qs:
            if is_dynamic_model and data[INHERITANCE_FIELD_NAME] in model_childs:
                yield model_childs[data[INHERITANCE_FIELD_NAME]](**data)
            else:
                yield cls(**data)

    @classmethod
    def __find_one(
        cls, filter: dict = {}, sort: Optional[List[Tuple[str, int]]] = None, **kwargs
    ) -> Optional[Self]:
        qs = cls.find_raw(filter, **kwargs)
        if sort:
            qs = qs.sort(sort)
        for data in qs.limit(1):
            """limit 1 is equivalent to find_one and that is implemented in pymongo find_one"""
            return cls(**data)
        return None

    @classmethod
    def get_or_create(
        cls, filter: dict = {}, session=None, **kwargs
    ) -> Tuple[Self, bool]:
        obj = cls.__find_one(filter)
        if obj:
            return obj, False
        return cls(**filter).create(session=session, **kwargs), True

    @classmethod
    def get(
        cls, filter: dict = {}, sort: Optional[List[Tuple[str, int]]] = None, **kwargs
    ) -> Self:
        obj = cls.__find_one(filter, sort=sort, **kwargs)
        if obj:
            return obj
        raise Exception("Object not found.")

    @classmethod
    def find_first(
        cls, filter: dict = {}, sort: Optional[List[Tuple[str, int]]] = None, **kwargs
    ) -> Optional[Self]:
        return cls.__find_one(filter, sort=sort, **kwargs)

    @classmethod
    def find_last(
        cls,
        filter: dict = {},
        sort: Optional[List[Tuple[str, int]]] = [("_id", DESCENDING)],
        **kwargs,
    ) -> Optional[Self]:
        return cls.__find_one(filter, sort=sort, **kwargs)

    @classmethod
    def count_documents(cls, filter: dict = {}, **kwargs) -> int:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {f"{INHERITANCE_FIELD_NAME}": cls._get_child(), **filter}
        return _collection.count_documents(filter, **kwargs)

    @classmethod
    def exists(cls, filter: dict = {}, **kwargs) -> bool:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {f"{INHERITANCE_FIELD_NAME}": cls._get_child(), **filter}
        return _collection.count_documents(filter, **kwargs, limit=1) >= 1

    @classmethod
    def aggregate(cls, pipeline: List[Any], **kwargs) -> CommandCursor:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            pipeline = [
                {"$match": {f"{INHERITANCE_FIELD_NAME}": cls._get_child()}}
            ] + pipeline
        return _collection.aggregate(pipeline, **kwargs)

    @classmethod
    def get_random_one(cls, filter: dict = {}, **kwargs) -> Optional[Self]:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter[INHERITANCE_FIELD_NAME] = cls._get_child()
        pipeline = [{"$match": filter}, {"$sample": {"size": 1}}]
        for data in _collection.aggregate(pipeline, **kwargs):
            return cls(**data)
        return None

    def update(self, raw: dict = {}, **kwargs) -> UpdateResult:
        _collection = self._get_collection()
        filter = {"_id": self.id}
        if raw:
            updated_data = raw
        else:
            updated_data = {"$set": self.dict(exclude={"id"})}
        if hasattr(self, "updated_at"):
            datetime_now = datetime.utcnow()
            updated_data["$set"]["updated_at"] = datetime_now
            self.__dict__.update({"updated_at": datetime_now})

        return _collection.update_one(filter, updated_data, **kwargs)

    @classmethod
    def update_one(cls, filter: dict = {}, data: dict = {}, **kwargs) -> UpdateResult:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {f"{INHERITANCE_FIELD_NAME}": cls._get_child(), **filter}
        return _collection.update_one(filter, data, **kwargs)

    @classmethod
    def update_many(cls, filter: dict = {}, data: dict = {}, **kwargs) -> UpdateResult:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {f"{INHERITANCE_FIELD_NAME}": cls._get_child(), **filter}
        return _collection.update_many(filter, data, **kwargs)

    def delete(self, **kwargs) -> DeleteResult:
        _collection = self._get_collection()
        return _collection.delete_one({"_id": self.id}, **kwargs)

    @classmethod
    def delete_many(cls, filter: dict = {}, **kwargs) -> DeleteResult:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {f"{INHERITANCE_FIELD_NAME}": cls._get_child(), **filter}
        return _collection.delete_many(filter, **kwargs)


__all__ = ["INHERITANCE_FIELD_NAME", "Document"]
