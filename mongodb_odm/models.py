from collections.abc import AsyncIterator, Iterator, Sequence
from datetime import datetime
from typing import (
    Any,
    Optional,
    Union,
    cast,
)

from mongodb_odm.connection import db, get_client
from mongodb_odm.data_conversion import dict2obj
from mongodb_odm.exceptions import InvalidConfiguration, ObjectDoesNotExist
from mongodb_odm.fields import Field
from mongodb_odm.types import DICT_TYPE, SORT_TYPE, ODMObjectId, WriteOp
from mongodb_odm.utils._internal_models import CollectionConfig, RelationalFieldInfo
from mongodb_odm.utils.utils import (
    convert_model_to_collection,
    get_database_name,
    get_model_fields,
    get_relationship_fields_info,
    transform_filter,
)
from mongodb_odm.utils.validation import validate_filter_dict
from pydantic import BaseModel, PrivateAttr
from pydantic._internal._model_construction import ModelMetaclass
from pymongo import AsyncMongoClient, IndexModel, MongoClient
from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import BulkWriteResult, DeleteResult, UpdateResult
from typing_extensions import Self

INHERITANCE_FIELD_NAME = "_cls"

RELATION_TYPE = dict[str, RelationalFieldInfo]

_cashed_collection: dict[Any, CollectionConfig] = {}
_cashed_field_info: dict[str, RELATION_TYPE] = {}


def _clear_cache() -> None:
    global _cashed_collection, _cashed_field_info
    for key in list(_cashed_collection.keys()):
        del _cashed_collection[key]

    for key in list(_cashed_field_info.keys()):
        del _cashed_field_info[key]


class ODMMeta(ModelMetaclass):
    def __getattr__(cls, name: str) -> Any:
        # Avoid recursion for internal pydantic attributes
        if name.startswith("__pydantic"):
            raise AttributeError(name)

        try:
            # Try to access model_fields without triggering __getattr__ for it
            # In Pydantic v2, fields are stored in __pydantic_fields__
            fields = cls.__dict__.get("__pydantic_fields__")

            if fields and name in fields:
                return name
        except Exception:
            pass

        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")


class _BaseDocument(BaseModel, metaclass=ODMMeta):
    """
    This class will handle all database and model-related configuration.
    """

    class ODMConfig:
        # Those fields will work as the default value of any child class.
        collection_name: Optional[str] = None
        allow_inheritance: bool = False
        index_inheritance_field: bool = True
        indexes: list[IndexModel] = []
        database: Optional[str] = None

        """
        Definition of ODMConfig fields:

        collection_name: This field will overwrite collection name.

        allow_inheritance: It enables a model to have a child.
        We will manage a single field for parent and child collection.
        The collection name will be according to the parent model configuration.
        Child collection data will be separated by field name '_cls'.

        index_inheritance_field: By default, we create an index for '_cls'
        if the model has a child. Users may control that by using this field.

        indexes: Define list of IndexModel to manage indexes for a model

        database: Handle multiple database configurations using this field.
        The default database will be None.
        """

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Add '# type: ignore' as a comment if get type error while getting this value
        """
        if key == "_id" or key == "id":
            self.__dict__["id"] = value
            self.__dict__["_id"] = value
        else:
            self.__dict__[key] = value

    def dict(self, **kwargs: Any) -> DICT_TYPE:
        return self.model_dump(**kwargs)

    @classmethod
    def __get_collection_class(cls) -> tuple[str, Optional[str]]:
        """
        Get model class.
        if called from a child class:
            return (parent-class, child-class)
        else:
            return (class, None)
        """
        model: Any = cls
        if model.__base__ != Document:
            base_model = model.__base__
            if (
                not hasattr(base_model.ODMConfig, "allow_inheritance")
                or base_model.ODMConfig.allow_inheritance is not True
            ):
                raise InvalidConfiguration(
                    f"Invalid model inheritance. {base_model} does not allow model inheritance."
                )
            if (
                base_model.ODMConfig.allow_inheritance is True
                and model.ODMConfig.allow_inheritance is True
            ):
                raise InvalidConfiguration(
                    f"Child Model{model.__name__} should declare a separate ODMConfig class."
                )
            return base_model, model
        else:
            return model, None

    @classmethod
    def __get_collection_config(cls) -> CollectionConfig:
        """
        Get collection configuration for a model.
        Get data from the cache if it is already calculated.
        """
        global _cashed_collection
        if cls in _cashed_collection:
            return _cashed_collection[cls]

        model, child_model = cls.__get_collection_class()

        has_children = False
        if (
            hasattr(cls.ODMConfig, "allow_inheritance")
            and cls.ODMConfig.allow_inheritance is True
        ):
            """Check if this is a model that allows inheritance and has a child model."""
            has_children = len(cls.__subclasses__()) > 0

        child_collection_name = (
            convert_model_to_collection(child_model) if child_model else None
        )
        _cashed_collection[cls] = CollectionConfig(
            collection_name=convert_model_to_collection(model),
            child_collection_name=child_collection_name,
            database_name=get_database_name(model),
            has_children=has_children,
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
        """
        Get the child collection name if it has a parent class.
        """
        return cls.__get_collection_config().child_collection_name

    @classmethod
    def _has_children(cls) -> bool:
        """
        Check if a model has child class
        """
        return cls.__get_collection_config().has_children

    @classmethod
    def _get_collection(cls) -> Collection[Any]:
        db_connection = db(cls._database_name())
        collection = db_connection[cls._get_collection_name()]

        return cast(Collection[Any], collection)

    @classmethod
    def _async_get_collection(cls) -> AsyncCollection[Any]:
        db_connection = db(cls._database_name(), is_async_action=True)
        collection = db_connection[cls._get_collection_name()]

        return cast(AsyncCollection[Any], collection)

    @classmethod
    def _db(cls) -> str:
        return cls._get_collection_name()

    @classmethod
    def get_inheritance_key(cls) -> DICT_TYPE:
        """
        Get child filter keys
        """
        return {INHERITANCE_FIELD_NAME: cls._get_child()}

    @classmethod
    def get_parent_child_fields(cls) -> DICT_TYPE:
        fields = get_model_fields(cls)
        if cls._has_children():
            for model in cls.__subclasses__():
                child_fields = get_model_fields(model)
                fields.update(child_fields)
        return fields

    @classmethod
    def get_relational_field_info(cls) -> RELATION_TYPE:
        """
        Get all relational field information.
        Get data from from cache if it's already calculated.
        """
        global _cashed_field_info
        field_info_key = f"{hash(cls)}-field_info"  # unique key for each model

        cached_field_info = _cashed_field_info.get(field_info_key)
        if not cached_field_info:
            cached_field_info = get_relationship_fields_info(cls)
            _cashed_field_info[field_info_key] = cached_field_info
        return cached_field_info

    @classmethod
    def get_exclude_fields(cls) -> set[str]:
        """
        Get all fields that should not pass while creating or updating an object.
        """
        relational_fields = cls.get_relational_field_info().keys()
        return {"_id", "id", *relational_fields}

    def to_mongo(self) -> DICT_TYPE:
        """
        relational-field: The relational field is only for representational use only.
        Do not store those fields in the database.

        id: For '_id' and 'id' fields will be excluded on the object creation.
        So that 'id' creation happens on the database only.

        None: Exclude null fields to improve database storage efficiency.
        """
        return self.dict(exclude=self.get_exclude_fields())

    @classmethod
    def start_session(cls, **kwargs: Any) -> ClientSession:
        client = get_client()
        if not isinstance(client, MongoClient):
            raise InvalidConfiguration(
                "Client is not configured for sync operations use 'astart_session' instead."
            )

        return client.start_session(**kwargs)

    @classmethod
    def astart_session(cls, **kwargs: Any) -> AsyncClientSession:
        client = get_client()
        if not isinstance(client, AsyncMongoClient):
            raise InvalidConfiguration(
                "Client is not configured for async operations use 'start_session' instead."
            )

        return client.start_session(**kwargs)

    def __str__(self) -> str:
        return super().__repr__()


class Document(_BaseDocument):
    """
    id: For '_id' and 'id' fields will be excluded on the object creation.
    So that 'id' creation happens on the database only.
    """

    _id: ODMObjectId = PrivateAttr(default_factory=ODMObjectId)
    id: ODMObjectId = Field(default_factory=ODMObjectId)

    def __init__(self, *args: list[Any], **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        if "_id" in kwargs:
            id = ODMObjectId(kwargs["_id"])
        elif "id" in kwargs:
            id = ODMObjectId(kwargs["id"])
        else:
            id = ODMObjectId()

        object.__setattr__(self, "id", id)
        object.__setattr__(self, "_id", id)

    def _prepare_crate_data(self, **kwargs: Any) -> DICT_TYPE:
        data = self.to_mongo()
        if self._get_child() is not None:
            # Assign the '_cls' field if the model is a child.
            data = {**self.get_inheritance_key(), **data}

        return data

    def _update_new_id(self, new_id: ODMObjectId) -> None:
        self.__dict__.update({"_id": new_id, "id": new_id})

    def create(self, **kwargs: Any) -> Self:
        data = self._prepare_crate_data(**kwargs)

        _collection = self._get_collection()
        result = _collection.insert_one(data, **kwargs)
        inserted_id = result.inserted_id
        self._update_new_id(inserted_id)

        return self

    async def acreate(self, **kwargs: Any) -> Self:
        data = self._prepare_crate_data(**kwargs)

        _collection = self._async_get_collection()
        inserted_id = (await _collection.insert_one(data, **kwargs)).inserted_id
        self._update_new_id(inserted_id)

        return self

    @classmethod
    def _validate_and_prepare_filter(cls, filter: Optional[DICT_TYPE]) -> DICT_TYPE:
        if filter is None:
            filter = {}

        transform_filter(filter)
        validate_filter_dict(cls, filter)

        if cls._get_child() is not None:
            filter = {**cls.get_inheritance_key(), **filter}

        return filter

    @classmethod
    def find_raw(
        cls,
        filter: Optional[DICT_TYPE] = None,
        projection: Optional[DICT_TYPE] = None,
        **kwargs: Any,
    ) -> Cursor[Any]:
        if projection is None:
            projection = {}

        filter = cls._validate_and_prepare_filter(filter)

        _collection = cls._get_collection()

        if projection:
            return _collection.find(filter, projection, **kwargs)

        return _collection.find(filter, **kwargs)

    @classmethod
    def afind_raw(
        cls,
        filter: Optional[DICT_TYPE] = None,
        projection: Optional[DICT_TYPE] = None,
        **kwargs: Any,
    ) -> AsyncCursor[Any]:
        if projection is None:
            projection = {}

        filter = cls._validate_and_prepare_filter(filter)
        _collection = cls._async_get_collection()

        if projection:
            return _collection.find(filter, projection, **kwargs)

        return _collection.find(filter, **kwargs)

    @classmethod
    def _prepare_query(
        cls,
        query_set: Any,
        sort: Optional[SORT_TYPE] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Any:
        """Helper method to prepare query with sort, skip and limit parameters."""
        if sort:
            query_set = query_set.sort(sort)
        if skip:
            query_set = query_set.skip(skip)
        if limit:
            query_set = query_set.limit(limit)

        return query_set

    @classmethod
    def _get_child_models(cls) -> dict[str, Self]:
        """Helper method to get child models mapping."""
        model_children: dict[str, Self] = {}

        for model in cls.__subclasses__():
            child_model_name = model._get_child()
            if child_model_name is None:
                continue

            model_children[child_model_name] = model  # type: ignore

        return model_children

    @classmethod
    def _prepare_class_instance(
        cls,
        model_children: dict[str, Self],
        data: DICT_TYPE,
    ) -> Self:
        if data.get(INHERITANCE_FIELD_NAME) in model_children:
            """If this is a child model then convert it to that child model."""
            kls = model_children[data[INHERITANCE_FIELD_NAME]]
            return kls(**data)  # type: ignore

        return cls(**data)

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
        qs = cls.find_raw(filter, projection, **kwargs)
        qs = cls._prepare_query(qs, sort, skip, limit)

        if cls._has_children():
            model_children = cls._get_child_models()
            for data in qs:
                yield cls._prepare_class_instance(model_children, data)
        else:
            for data in qs:
                yield cls(**data)

    @classmethod
    async def afind(
        cls,
        filter: Optional[DICT_TYPE] = None,
        projection: Optional[DICT_TYPE] = None,
        sort: Optional[SORT_TYPE] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncIterator[Self]:
        qs = cls.afind_raw(filter, projection, **kwargs)
        qs = cls._prepare_query(qs, sort, skip, limit)

        if cls._has_children():
            model_children = cls._get_child_models()
            async for data in qs:
                yield cls._prepare_class_instance(model_children, data)
        else:
            async for data in qs:
                yield cls(**data)

    @classmethod
    def find_one(
        cls,
        filter: Optional[DICT_TYPE] = None,
        projection: Optional[DICT_TYPE] = None,
        sort: Optional[SORT_TYPE] = None,
        **kwargs: Any,
    ) -> Optional[Self]:
        qs = cls.find_raw(filter, projection=projection, **kwargs)
        if sort:
            qs = qs.sort(sort)

        obj = None
        for data in qs.limit(1):
            """limit 1 is equivalent to find_one and that is implemented in pymongo find_one"""
            obj = data

        if not obj:
            return None

        if cls._has_children():
            model_children = cls._get_child_models()
            return cls._prepare_class_instance(model_children, data)

        return cls(**data)

    @classmethod
    async def afind_one(
        cls,
        filter: Optional[DICT_TYPE] = None,
        projection: Optional[DICT_TYPE] = None,
        sort: Optional[SORT_TYPE] = None,
        **kwargs: Any,
    ) -> Optional[Self]:
        qs = cls.afind_raw(filter, projection=projection, **kwargs)
        if sort:
            qs = qs.sort(sort)

        obj = None
        async for data in qs.limit(1):
            """limit 1 is equivalent to find_one and that is implemented in pymongo find_one"""
            obj = data

        if not obj:
            return None

        if cls._has_children():
            model_children = cls._get_child_models()
            return cls._prepare_class_instance(model_children, data)

        return cls(**data)

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
    async def aget(
        cls,
        filter: DICT_TYPE,
        sort: Optional[SORT_TYPE] = None,
        **kwargs: Any,
    ) -> Self:
        obj = await cls.afind_one(filter, sort=sort, **kwargs)
        if obj:
            return obj

        raise ObjectDoesNotExist("Object not found.")

    @classmethod
    def get_or_create(
        cls,
        filter: DICT_TYPE,
        sort: Optional[SORT_TYPE] = None,
        **kwargs: Any,
    ) -> tuple[Self, bool]:
        obj = cls.find_one(filter, sort=sort, **kwargs)
        if obj:
            return obj, False

        return cls(**filter).create(), True

    @classmethod
    async def aget_or_create(
        cls,
        filter: DICT_TYPE,
        sort: Optional[SORT_TYPE] = None,
        **kwargs: Any,
    ) -> tuple[Self, bool]:
        obj = await cls.afind_one(filter, sort=sort, **kwargs)
        if obj:
            return obj, False

        new_instance = await cls(**filter).acreate()

        return new_instance, True

    @classmethod
    def count_documents(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> int:
        filter = cls._validate_and_prepare_filter(filter)

        _collection = cls._get_collection()

        return _collection.count_documents(filter, **kwargs)

    @classmethod
    async def acount_documents(
        cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any
    ) -> int:
        filter = cls._validate_and_prepare_filter(filter)

        _collection = cls._async_get_collection()

        return await _collection.count_documents(filter, **kwargs)

    @classmethod
    def exists(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> bool:
        """
        It does not need to count all documents and avoid unnecessary db overhead.
        """
        for _ in cls.find_raw(filter, projection={"_id": 1}, **kwargs).limit(1):
            return True

        return False

    @classmethod
    async def aexists(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> bool:
        """
        It does not need to count all documents and avoid unnecessary db overhead.
        """
        async for _ in cls.afind_raw(filter, projection={"_id": 1}, **kwargs).limit(1):
            return True

        return False

    @classmethod
    def _prepare_aggregation_pipeline(
        cls,
        pipeline: list[Any],
        inheritance_filter: bool = True,
    ) -> list[Any]:
        if inheritance_filter and cls._get_child() is not None:
            """
            If aggregate was called from the child model then add the "$match" stage
            to separate the document from other child and parent.
            """
            if len(pipeline) > 0 and "$match" in pipeline[0]:
                """
                If the first stage of the pipeline is "$match"
                update it with the '_cls' field.
                """
                pipeline[0]["$match"] = {
                    f"{INHERITANCE_FIELD_NAME}": cls._get_child(),
                    **pipeline[0]["$match"],
                }
            else:
                pipeline = [
                    {"$match": {f"{INHERITANCE_FIELD_NAME}": cls._get_child()}}
                ] + pipeline

        return pipeline

    @classmethod
    def _get_aggregation_obj(cls, obj: DICT_TYPE, get_raw: bool = False) -> Any:
        if get_raw is True:
            return obj

        return dict2obj(obj)

    @classmethod
    def aggregate(
        cls,
        pipeline: list[Any],
        get_raw: bool = False,
        inheritance_filter: bool = True,
        **kwargs: Any,
    ) -> Iterator[Any]:
        pipeline = cls._prepare_aggregation_pipeline(
            pipeline, inheritance_filter=inheritance_filter
        )
        _collection = cls._get_collection()

        query = _collection.aggregate(pipeline, **kwargs)

        for obj in query:
            yield cls._get_aggregation_obj(obj, get_raw=get_raw)

    @classmethod
    async def aaggregate(
        cls,
        pipeline: list[Any],
        get_raw: bool = False,
        inheritance_filter: bool = True,
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        """
        Return an async iterator for MongoDB aggregation results.
        """
        pipeline = cls._prepare_aggregation_pipeline(
            pipeline, inheritance_filter=inheritance_filter
        )
        _collection = cls._async_get_collection()
        query = await _collection.aggregate(pipeline, **kwargs)

        async for obj in query:
            yield cls._get_aggregation_obj(obj, get_raw=get_raw)

    @classmethod
    def _get_pipeline_for_random_one(cls, filter: DICT_TYPE) -> list[DICT_TYPE]:
        return [{"$match": filter}, {"$sample": {"size": 1}}]

    @classmethod
    def get_random_one(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> Self:
        filter = cls._validate_and_prepare_filter(filter)
        pipeline = cls._get_pipeline_for_random_one(filter)

        for data in cls.aggregate(pipeline, get_raw=True, **kwargs):
            return cls(**data)

        raise ObjectDoesNotExist("Object not found.")

    @classmethod
    async def aget_random_one(
        cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any
    ) -> Self:
        filter = cls._validate_and_prepare_filter(filter)
        pipeline = cls._get_pipeline_for_random_one(filter)

        async for data in cls.aaggregate(pipeline, get_raw=True, **kwargs):
            return cls(**data)

        raise ObjectDoesNotExist("Object not found.")

    def _get_update_dict(self, raw: Optional[DICT_TYPE] = None) -> DICT_TYPE:
        if raw:
            updated_data = raw
        else:
            updated_data = {"$set": self.to_mongo()}

        if hasattr(self, "updated_at"):
            # Programmatically assign updated_at at the time of updating document.
            datetime_now = datetime.now()
            if "$set" not in updated_data:
                updated_data["$set"] = {}

            updated_data["$set"]["updated_at"] = datetime_now

            self.__dict__.update({"updated_at": datetime_now})

        return updated_data

    def update(self, raw: Optional[DICT_TYPE] = None, **kwargs: Any) -> UpdateResult:
        filter = {"_id": self.id}

        updated_data = self._get_update_dict(raw)

        return self.update_one(filter, updated_data, **kwargs)

    async def aupdate(
        self, raw: Optional[DICT_TYPE] = None, **kwargs: Any
    ) -> UpdateResult:
        filter = {"_id": self.id}

        updated_data = self._get_update_dict(raw)

        return await self.aupdate_one(filter, updated_data, **kwargs)

    @classmethod
    def update_one(
        cls, filter: DICT_TYPE, data: DICT_TYPE, **kwargs: Any
    ) -> UpdateResult:
        filter = cls._validate_and_prepare_filter(filter)

        _collection = cls._get_collection()

        return _collection.update_one(filter, data, **kwargs)

    @classmethod
    async def aupdate_one(
        cls, filter: DICT_TYPE, data: DICT_TYPE, **kwargs: Any
    ) -> UpdateResult:
        filter = cls._validate_and_prepare_filter(filter)
        _collection = cls._async_get_collection()

        return await _collection.update_one(filter, data, **kwargs)

    @classmethod
    def update_many(
        cls, filter: DICT_TYPE, data: DICT_TYPE, **kwargs: Any
    ) -> UpdateResult:
        filter = cls._validate_and_prepare_filter(filter)

        _collection = cls._get_collection()

        return _collection.update_many(filter, data, **kwargs)

    @classmethod
    async def aupdate_many(
        cls, filter: DICT_TYPE, data: DICT_TYPE, **kwargs: Any
    ) -> UpdateResult:
        filter = cls._validate_and_prepare_filter(filter)
        _collection = cls._async_get_collection()

        return await _collection.update_many(filter, data, **kwargs)

    def delete(self, **kwargs: Any) -> DeleteResult:
        return self.delete_one({"_id": self.id}, **kwargs)

    async def adelete(self, **kwargs: Any) -> DeleteResult:
        return await self.adelete_one({"_id": self.id}, **kwargs)

    @classmethod
    def delete_one(cls, filter: DICT_TYPE, **kwargs: Any) -> DeleteResult:
        """Will perform as Pymongo delete_one function."""
        filter = cls._validate_and_prepare_filter(filter)

        print(f"delete_many filter: {filter}, kwargs: {kwargs}")

        _collection = cls._get_collection()
        return _collection.delete_one(filter, **kwargs)

    @classmethod
    async def adelete_one(cls, filter: DICT_TYPE, **kwargs: Any) -> DeleteResult:
        """Will perform as Pymongo delete_one function."""
        filter = cls._validate_and_prepare_filter(filter)
        _collection = cls._async_get_collection()

        return await _collection.delete_one(filter, **kwargs)

    @classmethod
    def delete_many(cls, filter: DICT_TYPE, **kwargs: Any) -> DeleteResult:
        """Will perform as Pymongo delete_many function."""
        filter = cls._validate_and_prepare_filter(filter)

        _collection = cls._get_collection()
        return _collection.delete_many(filter, **kwargs)

    @classmethod
    async def adelete_many(cls, filter: DICT_TYPE, **kwargs: Any) -> DeleteResult:
        """Will perform as Pymongo delete_many function."""
        filter = cls._validate_and_prepare_filter(filter)
        _collection = cls._async_get_collection()

        return await _collection.delete_many(filter, **kwargs)

    @classmethod
    def bulk_write(
        cls, requests: Sequence[WriteOp[Any]], **kwargs: Any
    ) -> BulkWriteResult:
        _collection = cls._get_collection()
        return _collection.bulk_write(requests, **kwargs)

    @classmethod
    async def abulk_write(
        cls, requests: Sequence[WriteOp[Any]], **kwargs: Any
    ) -> BulkWriteResult:
        _collection = cls._async_get_collection()

        return await _collection.bulk_write(requests, **kwargs)

    @classmethod
    def _get_loadable_fields_info(
        cls,
        fields: Optional[list[str]] = None,
    ) -> RELATION_TYPE:
        """Get model relational field from cache"""
        cached_field_info = cls.get_relational_field_info()

        """Match with user given fields"""
        loadable_fields_info: Optional[RELATION_TYPE] = None
        if fields:
            loadable_fields_info = {}
            for field in fields:
                if field not in cached_field_info:
                    raise Exception(f'Invalid field "{field}"')
                loadable_fields_info[field] = cached_field_info[field]
        else:
            loadable_fields_info = {**cached_field_info}

        return loadable_fields_info

    @classmethod
    def _get_instance_related_info(
        cls, loadable_fields_info: RELATION_TYPE
    ) -> tuple[dict[str, list[Any]], DICT_TYPE]:
        field_keys = loadable_fields_info.keys()

        fields_id_dict: dict[str, list[RELATION_TYPE]] = {
            field: [] for field in field_keys
        }
        field_data_data: DICT_TYPE = {field: {} for field in field_keys}

        return fields_id_dict, field_data_data

    @classmethod
    def _get_objects_and_update_fields_id(
        cls,
        object_list: Union[Iterator[Self], Sequence[Self]],
        loadable_fields_info: RELATION_TYPE,
        fields_id_dict: dict[str, list[Any]],
    ) -> list[Self]:
        results: list[Self] = []
        for obj in object_list:
            for field, field_info in loadable_fields_info.items():
                fields_id_dict[field].append(obj.__dict__[field_info.local_field])

            results.append(obj)

        return results

    @classmethod
    def load_related(
        cls,
        object_list: Union[Iterator[Self], Sequence[Self]],
        fields: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> Sequence[Self]:
        """
        This method will load related documents from the database
        according to the specified fields.
        """
        if fields is None:
            fields = []

        loadable_fields_info = cls._get_loadable_fields_info(fields)
        fields_id_dict, field_data_data = cls._get_instance_related_info(
            loadable_fields_info
        )
        results = cls._get_objects_and_update_fields_id(
            object_list, loadable_fields_info, fields_id_dict
        )

        """Load all document for all relational model"""
        for field, ids in fields_id_dict.items():
            query = loadable_fields_info[field].model.find({"_id": {"$in": ids}})

            field_data_data[field] = {obj.id: obj for obj in query}

        """Assign loaded document with results"""
        for obj in results:
            for field, field_info in loadable_fields_info.items():
                field_obj = field_data_data[field].get(
                    obj.__dict__[field_info.local_field]
                )
                obj.__dict__[field] = field_obj

        return results

    @classmethod
    async def _async_get_objects_and_update_fields_id(
        cls,
        object_list: AsyncIterator[Self],
        loadable_fields_info: RELATION_TYPE,
        fields_id_dict: dict[str, list[Any]],
    ) -> list[Self]:
        results: list[Self] = []
        async for obj in object_list:
            for field, field_info in loadable_fields_info.items():
                fields_id_dict[field].append(obj.__dict__[field_info.local_field])

            results.append(obj)

        return results

    @classmethod
    async def aload_related(
        cls,
        object_list: AsyncIterator[Self],
        fields: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> Sequence[Self]:
        """
        This method will load related documents from the database
        according to the specified fields.
        """
        if fields is None:
            fields = []

        loadable_fields_info = cls._get_loadable_fields_info(fields)
        fields_id_dict, field_data_data = cls._get_instance_related_info(
            loadable_fields_info
        )
        results = await cls._async_get_objects_and_update_fields_id(
            object_list, loadable_fields_info, fields_id_dict
        )

        """Load all document for all relational model"""
        for field, ids in fields_id_dict.items():
            query = loadable_fields_info[field].model.afind({"_id": {"$in": ids}})

            field_data_data[field] = {obj.id: obj async for obj in query}

        """Assign loaded document with results"""
        for obj in results:
            for field, field_info in loadable_fields_info.items():
                field_obj = field_data_data[field].get(
                    obj.__dict__[field_info.local_field]
                )
                obj.__dict__[field] = field_obj

        return results
