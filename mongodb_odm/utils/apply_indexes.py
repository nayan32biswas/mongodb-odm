import logging
from collections.abc import MutableMapping
from typing import Any, Optional, Union

from bson import SON
from mongodb_odm.connection import db
from mongodb_odm.exceptions import ConnectionError, InvalidConnection
from mongodb_odm.models import INHERITANCE_FIELD_NAME, Document
from mongodb_odm.types import DICT_TYPE
from pydantic import BaseModel
from pymongo import ASCENDING, TEXT, IndexModel
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

logger = logging.getLogger(__name__)

DatabaseIndexesType = CommandCursor[MutableMapping[str, Any]]


class IndexOperation(BaseModel):
    collection_name: str
    model_indexes: list[Any]
    database_name: Optional[str] = None


def _get_dict_db_indexes(database_indexes: DatabaseIndexesType) -> list[DICT_TYPE]:
    dict_db_indexes: list[DICT_TYPE] = []

    for index in database_indexes:
        old_index = index.to_dict()  # type: ignore
        # Skip "_id" index since it's create by mongodb system
        if "_id" in old_index["key"]:
            continue

        old_index.pop("v", None)
        dict_db_indexes.append(old_index)

    return dict_db_indexes


def _get_dict_model_indexes(
    model_indexes: list[IndexModel],
) -> tuple[list[DICT_TYPE | None], dict[str, IndexModel]]:
    dict_model_indexes: list[DICT_TYPE | None] = []
    model_indexes_map: dict[str, IndexModel] = {}

    for index in model_indexes:
        new_index: Any = index.document
        # Replace SON object with dict
        if isinstance(new_index["key"], SON):
            new_index["key"] = new_index["key"].to_dict()
        if isinstance(new_index["key"], dict):
            new_index["key"] = new_index["key"]
        else:
            continue
        dict_model_indexes.append(new_index)
        # Store index object for future use
        model_indexes_map[new_index["name"]] = index

    return dict_model_indexes, model_indexes_map


def _check_exists_in_model_indexes(
    db_dict_index: DICT_TYPE, dict_model_indexes: list[DICT_TYPE | None]
) -> bool:
    def mark_as_exist(position: int) -> bool:
        """
        Since the index already exists in the model indexes,
        we will mark it as None.
        """
        dict_model_indexes[position] = None

        return True

    # Iterate over the indexes that are currently assigned in the model
    for idx, index_obj in enumerate(dict_model_indexes):
        if not index_obj or not isinstance(index_obj, dict):
            continue

        if db_dict_index == index_obj:
            mark_as_exist(idx)
            return True

        if db_dict_index.get("name") == index_obj.get("name"):
            # This condition will handle some of the special indexes like text-based indexes.
            db_value, new_value = db_dict_index, index_obj
            if TEXT in db_value["key"].values() and TEXT in new_value["key"].values():
                """
                based on condition this is a text-based index.
                Check that if value is changed.
                If not changed then assign null otherwise not.
                NOTE:
                The data check may not be sufficient enough.
                Add conditions based on the issue.
                """

                new_keys = new_value["key"].keys()
                default_language = new_value.get("default_language", "english")
                new_weight = new_value.get("weights") or dict.fromkeys(new_keys, 1)

                if (
                    db_value["weights"].keys() == new_keys
                    and new_weight == db_value["weights"]
                    and db_value["default_language"] == default_language
                ):
                    """Check all key, weights, and default_language match with existing values"""
                    mark_as_exist(idx)
                    return True

    return False


def _get_calculated_indexes_for_collection(
    database_indexes: DatabaseIndexesType,
    model_indexes: list[IndexModel],
) -> tuple[list[IndexModel], list[DICT_TYPE]]:
    dict_db_indexes = _get_dict_db_indexes(database_indexes)
    dict_model_indexes, model_indexes_map = _get_dict_model_indexes(model_indexes)

    delete_db_indexes: list[DICT_TYPE] = []

    # Iterate over indexes that are already created for a collection
    for db_dict_index in dict_db_indexes:
        is_matched = _check_exists_in_model_indexes(db_dict_index, dict_model_indexes)

        if not is_matched:
            # If the index does not exist in model indexes then delete it.
            delete_db_indexes.append(db_dict_index)

    new_indexes = [
        model_indexes_map[new_index["name"]]
        for new_index in dict_model_indexes
        if new_index
    ]

    return new_indexes, delete_db_indexes


def _get_model_indexes(model: type[Document]) -> list[IndexModel]:
    # Get define indexes for a model
    if hasattr(model.ODMConfig, "indexes"):
        return list(model.ODMConfig.indexes)
    return []


def _get_all_indexes() -> list[IndexOperation]:
    """
    First imports all child models of Document since it's the abstract parent model.
    Then retrieve all the child modules and will try to get indexes inside the ODMConfig class.
    """
    operations: list[IndexOperation] = []

    def get_operation_obj(model: type[Document]) -> IndexOperation:
        return IndexOperation(
            collection_name=model._get_collection_name(),
            model_indexes=_get_model_indexes(model),
            database_name=model._database_name(),
        )

    for model in Document.__subclasses__():
        obj = get_operation_obj(model)
        if (
            hasattr(model.ODMConfig, "allow_inheritance")
            and model.ODMConfig.allow_inheritance is True
        ):
            """If a model has child model"""
            if model.ODMConfig.index_inheritance_field is True:
                """
                If index_inheritance_field is true then create an index '_cls'
                    that will store the name of the child collection name.
                """
                obj.model_indexes.append(
                    IndexModel([(INHERITANCE_FIELD_NAME, ASCENDING)])
                )
            for child_model in model.__subclasses__():
                """Get all indexes that are defined in child model"""
                obj.model_indexes += _get_model_indexes(child_model)

        if obj and obj.model_indexes:
            operations.append(obj)

    return operations


def _get_collection(
    operation: IndexOperation,
) -> Union[Collection[Any], AsyncCollection[Any]]:
    return db(operation.database_name)[operation.collection_name]


def _get_created_and_deleted_indexes_count(
    operation: IndexOperation,
    new_indexes: list[IndexModel],
    delete_db_indexes: list[DICT_TYPE],
) -> tuple[int, int]:
    ne, de = len(new_indexes), len(delete_db_indexes)
    if ne > 0 or de > 0:
        logger.info(
            f'Applied for "{operation.collection_name}": {de} deleted, {ne} added'
        )

    return ne, de


def _get_collection_and_indexes(
    operation: IndexOperation,
) -> tuple[Union[Collection[Any], AsyncCollection[Any]], list[IndexModel]]:
    try:
        collection = _get_collection(operation)
        model_indexes = operation.model_indexes
    except Exception as e:
        raise InvalidConnection(
            f"Invalid database:'{operation.database_name}' and collection:{operation.collection_name}"
        ) from e

    return collection, model_indexes


def _sync_get_database_indexes(
    collection: Union[Collection[Any], AsyncCollection[Any]],
) -> CommandCursor[MutableMapping[str, Any]]:
    if isinstance(collection, Collection):
        return collection.list_indexes()

    if isinstance(collection, AsyncCollection):
        raise ConnectionError("Use synchronous collection for indexes.")


def _sync_apply_indexes_to_db(
    operation: IndexOperation,
    new_indexes: list[IndexModel],
    delete_db_indexes: list[DICT_TYPE],
) -> tuple[int, int]:
    collection = _get_collection(operation)

    for db_index in delete_db_indexes:
        # If the DB index does not exist in new_indexes then drop that index.
        if db_index is not None:
            collection.drop_index(db_index["name"])

    if len(new_indexes) > 0:
        try:
            collection.create_indexes(new_indexes)
        except Exception as e:
            logger.error(f'\nProblem arise at "{operation.collection_name}": {e}\n')
            raise e

    return _get_created_and_deleted_indexes_count(
        operation, new_indexes, delete_db_indexes
    )


def _sync_apply_indexes_for_a_collection(operation: IndexOperation) -> tuple[int, int]:
    collection, model_indexes = _get_collection_and_indexes(operation)
    database_indexes = _sync_get_database_indexes(collection)
    new_indexes, delete_db_indexes = _get_calculated_indexes_for_collection(
        database_indexes, model_indexes
    )
    ne, de = _sync_apply_indexes_to_db(operation, new_indexes, delete_db_indexes)

    return ne, de


def log_final_results(new_index: int, delete_index: int) -> None:
    if delete_index:
        logger.info(f"{delete_index}, index deleted.")
    if new_index:
        logger.info(f"{new_index}, index created.")
    if [new_index, delete_index] == [0, 0]:
        logger.info("No change detected.")


def apply_indexes() -> None:
    """First get all indexes from all model."""
    operations = _get_all_indexes()

    """Then execute each indexes operation for each model."""
    new_index, delete_index = 0, 0
    for operation in operations:
        ne, de = _sync_apply_indexes_for_a_collection(operation)
        new_index += ne
        delete_index += de

    log_final_results(new_index, delete_index)
