import logging
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional, Sequence, Set, Tuple, Union

from bson import ObjectId
from pydantic import BaseModel
from pymongo import IndexModel, client_session
from pymongo.collection import Collection, _WriteOp
from pymongo.cursor import Cursor
from pymongo.results import BulkWriteResult, DeleteResult, UpdateResult
from typing_extensions import Self

from .connection import db, get_client
from .data_conversion import dict2obj
from .exceptions import ObjectDoesNotExist
from .fields import Field
from .types import DICT_TYPE, SORT_TYPE, ODMObjectId
from .utils._internal_models import CollectionConfig, RelationalFieldInfo
from .utils.utils import (
    convert_model_to_collection,
    get_database_name,
    get_relationship_fields_info,
)

logger = logging.getLogger(__name__)
INHERITANCE_FIELD_NAME = "_cls"

RELATION_TYPE = Dict[str, RelationalFieldInfo]

_cashed_collection: Dict[Any, CollectionConfig] = {}
_cashed_field_info: Dict[str, RELATION_TYPE] = {}


def _clear_cache() -> None:
    global _cashed_collection, _cashed_field_info
    for key in [key for key in _cashed_collection.keys()]:
        del _cashed_collection[key]

    for key in [key for key in _cashed_field_info.keys()]:
        del _cashed_field_info[key]


class _BaseDocument(BaseModel):
    class Config:
        # Those fields will work as the default value of any child class.
        orm_mode: bool = True
        allow_population_by_field_name: bool = True
        collection_name: Optional[str] = None
        allow_inheritance: bool = False
        index_inheritance_field: bool = True
        indexes: List[IndexModel] = []
        database: Optional[str] = None

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Add '# type: ignore' as a comment if get type error while getting this value
        """
        self.__dict__[key] = value

    @classmethod
    def __get_collection_class(cls) -> Tuple[str, Optional[str]]:
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
            if (
                base_model.Config.allow_inheritance is True
                and model.Config.allow_inheritance is True
            ):
                raise Exception(
                    f"Child Model{model.__name__} should declare a separate Config class."
                )
            return base_model, model
        else:
            return model, None

    @classmethod
    def __get_collection_config(cls) -> CollectionConfig:
        global _cashed_collection
        if cls in _cashed_collection:
            return _cashed_collection[cls]

        model, child_model = cls.__get_collection_class()
        _cashed_collection[cls] = CollectionConfig(
            collection_name=convert_model_to_collection(model),
            child_collection_name=convert_model_to_collection(child_model)
            if child_model
            else None,
            database_name=get_database_name(model),
        )
        return _cashed_collection[cls]

    @classmethod
    def _database_name(cls) -> Optional[str]:
        config = cls.__get_collection_config()
        return config.database_name

    @classmethod
    def _get_collection_name(cls) -> str:
        return cls.__get_collection_config().collection_name

    @classmethod
    def _get_child(cls) -> Optional[str]:
        return cls.__get_collection_config().child_collection_name

    @classmethod
    def _get_collection(cls) -> Collection[Any]:
        return db(cls._database_name())[cls._get_collection_name()]

    @classmethod
    def _db(cls) -> str:
        return cls._get_collection_name()

    @classmethod
    def get_inheritance_key(cls) -> Dict[str, Optional[str]]:
        return {INHERITANCE_FIELD_NAME: cls._get_child()}

    @classmethod
    def get_relational_field_info(cls) -> RELATION_TYPE:
        global _cashed_field_info
        field_info_key = f"{hash(cls)}-field_info"

        cached_field_info = _cashed_field_info.get(field_info_key)
        if not cached_field_info:
            cached_field_info = get_relationship_fields_info(cls)
            _cashed_field_info[field_info_key] = cached_field_info
        return cached_field_info

    @classmethod
    def get_exclude_fields(cls) -> Set[str]:
        relational_fields = cls.get_relational_field_info().keys()
        return {"_id", "id", *relational_fields}

    # @classmethod
    # def to_mongo(cls, self_obj) -> dict:
    #     return self_obj.dict(
    #         exclude=cls.get_exclude_fields(), exclude_none=True
    #     )

    def to_mongo(self) -> DICT_TYPE:
        return self.dict(exclude=self.get_exclude_fields(), exclude_none=True)

    @classmethod
    def start_session(cls, **kwargs: Any) -> client_session.ClientSession:
        return get_client().start_session(**kwargs)

    def __str__(self) -> str:
        return super().__repr__()


class Document(_BaseDocument):
    _id: ODMObjectId = Field(default_factory=ObjectId)
    id: ODMObjectId = Field(default_factory=ObjectId, alias="_id")

    def __init__(self, *args: List[Any], **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if "_id" in kwargs:
            object.__setattr__(self, "_id", kwargs["_id"])
        else:
            object.__setattr__(self, "_id", self._id.default_factory())  # type: ignore

    def create(self, **kwargs: Any) -> Self:
        _collection = self._get_collection()

        data = self.to_mongo()
        if self._get_child() is not None:
            data = {**self.get_inheritance_key(), **data}

        inserted_id = _collection.insert_one(data, **kwargs).inserted_id
        self.__dict__.update({"_id": inserted_id, "id": inserted_id})
        return self

    @classmethod
    def find_raw(
        cls,
        filter: Optional[DICT_TYPE] = None,
        projection: Optional[DICT_TYPE] = None,
        **kwargs: Any,
    ) -> Cursor[Any]:
        if filter is None:
            filter = {}
        if projection is None:
            projection = {}

        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}
        if projection:
            return _collection.find(filter, projection, **kwargs)
        return _collection.find(filter, **kwargs)

    @classmethod
    def find(
        cls,
        filter: Optional[DICT_TYPE] = None,
        projection: Optional[DICT_TYPE] = None,
        sort: Optional[SORT_TYPE] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> Iterator[Self]:
        if filter is None:
            filter = {}

        qs = cls.find_raw(filter, projection, **kwargs)
        if sort:
            qs = qs.sort(sort)
        if skip:
            qs = qs.skip(skip)
        if limit:
            qs = qs.limit(limit)

        model_children = {}
        is_dynamic_model = False
        if (
            hasattr(cls.Config, "allow_inheritance")
            and cls.Config.allow_inheritance is True
        ):
            is_dynamic_model = True
            for model in cls.__subclasses__():
                model_children[model._get_child()] = model

        for data in qs:
            if is_dynamic_model and data.get(INHERITANCE_FIELD_NAME) in model_children:
                yield model_children[data[INHERITANCE_FIELD_NAME]](**data)
            else:
                yield cls(**data)

    @classmethod
    def find_one(
        cls,
        filter: Optional[DICT_TYPE] = None,
        projection: Optional[DICT_TYPE] = None,
        sort: Optional[SORT_TYPE] = None,
        **kwargs: Any,
    ) -> Optional[Self]:
        if filter is None:
            filter = {}

        qs = cls.find_raw(filter, projection=projection, **kwargs)
        if sort:
            qs = qs.sort(sort)
        for data in qs.limit(1):
            """limit 1 is equivalent to find_one and that is implemented in pymongo find_one"""
            return cls(**data)
        return None

    @classmethod
    def get(
        cls,
        filter: DICT_TYPE,
        sort: Optional[SORT_TYPE] = None,
        **kwargs: Any,
    ) -> Self:
        obj = cls.find_one(filter, sort=sort, **kwargs)
        if obj:
            return obj
        raise ObjectDoesNotExist("Object not found.")

    @classmethod
    def get_or_create(
        cls,
        filter: DICT_TYPE,
        sort: Optional[SORT_TYPE] = None,
        **kwargs: Any,
    ) -> Tuple[Self, bool]:
        obj = cls.find_one(filter, sort=sort, **kwargs)
        if obj:
            return obj, False
        return cls(**filter).create(), True

    @classmethod
    def count_documents(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> int:
        if filter is None:
            filter = {}

        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}
        return _collection.count_documents(filter, **kwargs)

    @classmethod
    def exists(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> bool:
        if filter is None:
            filter = {}

        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}
        return _collection.count_documents(filter, **kwargs, limit=1) >= 1

    @classmethod
    def aggregate(
        cls,
        pipeline: List[Any],
        get_raw: bool = False,
        inheritance_filter: bool = True,
        **kwargs: Any,
    ) -> Iterator[Any]:
        _collection = cls._get_collection()
        if inheritance_filter and cls._get_child() is not None:
            if len(pipeline) > 0 and "$match" in pipeline[0]:
                pipeline[0]["$match"] = {
                    f"{INHERITANCE_FIELD_NAME}": cls._get_child(),
                    **pipeline[0]["$match"],
                }
            else:
                pipeline = [
                    {"$match": {f"{INHERITANCE_FIELD_NAME}": cls._get_child()}}
                ] + pipeline
        for obj in _collection.aggregate(pipeline, **kwargs):
            if get_raw is True:
                yield obj
            else:
                yield dict2obj(obj)

    @classmethod
    def get_random_one(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> Self:
        if filter is None:
            filter = {}

        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}
        pipeline = [{"$match": filter}, {"$sample": {"size": 1}}]
        for data in cls.aggregate(pipeline, get_raw=True, **kwargs):
            return cls(**data)
        raise ObjectDoesNotExist("Object not found.")

    def update(self, raw: Optional[DICT_TYPE] = None, **kwargs: Any) -> UpdateResult:
        filter = {"_id": self._id}
        if raw:
            updated_data = raw
        else:
            updated_data = {"$set": self.to_mongo()}
        if hasattr(self, "updated_at"):
            datetime_now = datetime.utcnow()
            if "$set" not in updated_data:
                updated_data["$set"] = {}
            updated_data["$set"]["updated_at"] = datetime_now
            self.__dict__.update({"updated_at": datetime_now})

        return self.update_one(filter, updated_data, **kwargs)

    @classmethod
    def update_one(
        cls, filter: DICT_TYPE, data: DICT_TYPE, **kwargs: Any
    ) -> UpdateResult:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}
        return _collection.update_one(filter, data, **kwargs)

    @classmethod
    def update_many(
        cls, filter: DICT_TYPE, data: DICT_TYPE, **kwargs: Any
    ) -> UpdateResult:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}
        return _collection.update_many(filter, data, **kwargs)

    def delete(self, **kwargs: Any) -> DeleteResult:
        return self.delete_one({"_id": self._id}, **kwargs)

    @classmethod
    def delete_one(cls, filter: DICT_TYPE, **kwargs: Any) -> DeleteResult:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}
        return _collection.delete_one(filter, **kwargs)

    @classmethod
    def delete_many(cls, filter: DICT_TYPE, **kwargs: Any) -> DeleteResult:
        _collection = cls._get_collection()
        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}
        return _collection.delete_many(filter, **kwargs)

    @classmethod
    def bulk_write(
        cls, requests: Sequence[_WriteOp[Any]], **kwargs: Any
    ) -> BulkWriteResult:
        _collection = cls._get_collection()
        return _collection.bulk_write(requests, **kwargs)

    @classmethod
    def load_related(
        cls,
        object_list: Union[Iterator[Self], Sequence[Self]],
        fields: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Sequence[Self]:
        if fields is None:
            fields = []

        """Get model relational field from cache"""
        cached_field_info = cls.get_relational_field_info()

        """Match with user given fields"""
        loadable_fields_info: Optional[DICT_TYPE] = None
        if fields:
            loadable_fields_info = {}
            for field in fields:
                if field not in cached_field_info:
                    raise Exception(f'Invalid field "{field}"')
                loadable_fields_info[field] = cached_field_info[field]
        else:
            loadable_fields_info = {**cached_field_info}

        field_keys = loadable_fields_info.keys()
        fields_id_dict: Dict[str, List[RELATION_TYPE]] = {
            field: [] for field in field_keys
        }

        """Load all necessary id from given object_list"""
        results = []
        for obj in object_list:
            for field, field_info in loadable_fields_info.items():
                fields_id_dict[field].append(obj.__dict__[field_info.local_field])
            results.append(obj)

        """Load all document for all relational model"""
        field_data_data: DICT_TYPE = {field: {} for field in field_keys}
        for field, ids in fields_id_dict.items():
            field_data_data[field] = {
                obj.id: obj
                for obj in loadable_fields_info[field].model.find({"_id": {"$in": ids}})
            }

        """Assign loaded document with results"""
        for obj in results:
            for field, field_info in loadable_fields_info.items():
                obj.__dict__[field] = field_data_data[field].get(
                    obj.__dict__[field_info.local_field]
                )

        return results
