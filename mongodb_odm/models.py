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


from .fields import PydanticDBRef as _PydanticDBRef
from .types import PydanticObjectId as _PydanticObjectId
from .utils import camel_to_snake
from .connection import get_db, get_client


INHERITANCE_FIELD_NAME = "_cls"


class Object:
    def from_list(self, values) -> List[Any]:
        temp = []
        for v in values:
            if isinstance(v, dict):
                temp.append(Object(**v))
            elif isinstance(v, list) or isinstance(v, tuple):
                temp.append(self.from_list(v))
            else:
                temp.append(v)
        return temp

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        for k, v in kwargs.items():
            if isinstance(v, dict):
                # setattr(self, k, Object(**v))
                self.__dict__[k] = Object(**v)
            elif isinstance(v, list) or isinstance(v, tuple):
                # setattr(self, k, self.from_list(v))
                self.__dict__[k] = self.from_list(v)
            else:
                # setattr(self, k, v)
                self.__dict__[k] = v

    def __repr__(self) -> str:
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__


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
    id: _PydanticObjectId = Field(default_factory=ObjectId, alias="_id")

    @property
    def ref(self) -> _PydanticDBRef:
        collection_name = self._get_collection_name()
        return _PydanticDBRef(collection=collection_name, id=self.id)

    def create(self, get_obj=False, **kwargs) -> Self:
        _collection = self._get_collection()

        data = self.dict(exclude={"id"})
        if self._get_child() is not None:
            data = {f"{INHERITANCE_FIELD_NAME}": self._get_child(), **data}

        inserted_id = _collection.insert_one(data, **kwargs).inserted_id
        if get_obj is True:
            data: Any = _collection.find_one({"_id": inserted_id}, **kwargs)
            model = self.__class__
            obj = model(**data)
            self.__dict__.update(obj.dict())
            return obj
        else:
            self.__dict__.update({"id": inserted_id})
            return self

    @classmethod
    def get_or_create(cls, session=None, **kwargs) -> Tuple[Self, bool]:
        obj = cls.find_last(kwargs)
        if obj:
            return obj, False
        return cls(**kwargs).create(session=session), True

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

    # @classmethod
    # def find_one_old(cls, filter: dict = {}, raw=False, **kwargs) -> Optional[Any]:
    #     _collection = cls._get_collection()
    #     if cls._get_child() is not None:
    #         filter = {f"{INHERITANCE_FIELD_NAME}": cls._get_child(), **filter}
    #     data = _collection.find_one(filter, **kwargs)
    #     if data:
    #         if raw:
    #             return data
    #         else:
    #             return cls(**data)
    #     else:
    #         return None

    @classmethod
    def find_one(
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
    def find_first(
        cls, filter: dict = {}, sort: Optional[List[Tuple[str, int]]] = None, **kwargs
    ) -> Optional[Self]:
        return cls.find_one(filter, sort=sort, **kwargs)

    @classmethod
    def find_last(
        cls,
        filter: dict = {},
        sort: Optional[List[Tuple[str, int]]] = [("_id", DESCENDING)],
        **kwargs,
    ) -> Optional[Self]:
        return cls.find_one(filter, sort=sort, **kwargs)

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


def convert_model_to_collection(model: Any) -> str:
    if (
        hasattr(model.Config, "collection_name")
        and model.Config.collection_name is not None
    ):
        """By default model has Config in Basemodel"""
        return model.Config.collection_name
    else:
        return camel_to_snake(model.__name__)


__all__ = ["INHERITANCE_FIELD_NAME", "Document"]
