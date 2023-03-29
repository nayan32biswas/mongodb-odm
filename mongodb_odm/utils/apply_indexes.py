import logging
from typing import List

from bson import SON
from pymongo import ASCENDING, IndexModel

from ..connection import db
from ..models import INHERITANCE_FIELD_NAME, Document

logger = logging.getLogger(__name__)


def index_for_a_collection(operation):
    """
    First get all indexes for a collection and match with operation.
    Remove full match object.

    If db_index partially match with operation_index then recreate/update it.

    For new_indexes unmatched with db_indexes create new index.
    For db_indexes unmatched with new_indexes drop indexes.
    """
    try:
        collection = db()[operation["collection_name"]]
        indexes = operation["create_indexes"]
    except Exception:
        raise Exception("Invalid index object")

    db_indexes = []
    for index in collection.list_indexes():
        temp_val = index.to_dict()  # type: ignore
        # Skip "_id" index since it's create by mongodb system
        if "_id" in temp_val["key"]:
            continue
        temp_val.pop("v", None)
        db_indexes.append(temp_val)

    new_indexes = []
    new_indexes_store = {}

    for index in indexes:
        temp_val = index.document
        # Replace SON object with dict
        if type(temp_val["key"]) == SON:
            temp_val["key"] = temp_val["key"].to_dict()
        else:
            continue
        new_indexes.append(temp_val)
        # Store index object for future use
        new_indexes_store[temp_val["name"]] = index

    update_indexes = []
    for i in range(len(db_indexes)):
        partial_match = None
        for j in range(len(new_indexes)):
            if type(new_indexes[j]) is not dict:
                continue
            if db_indexes[i] == new_indexes[j]:
                db_indexes[i], new_indexes[j] = None, None
                partial_match = None
                break

            """
            # TODO: make a list for partial match
            if partial match db_indexes[i] with new_indexes[i]:
                partial_match = j
                # not break here check if any other match exist
            """

        if partial_match is not None:
            update_indexes.append((db_indexes[i], new_indexes[partial_match]))
            db_indexes[i], new_indexes[partial_match] = None, None

    delete_db_indexes = [val for val in db_indexes if val]
    new_indexes = [val for val in new_indexes if val]

    for db_index in delete_db_indexes:
        if db_index is not None:
            collection.drop_index(db_index["name"])
    if len(new_indexes) > 0:
        new_indexes = [
            new_indexes_store[new_index["name"]]
            for new_index in new_indexes
            if new_index
        ]
        try:
            collection.create_indexes(new_indexes)
        except Exception as e:
            logger.error(f'\nProblem arise at "{operation["collection_name"]}": {e}\n')
            raise e

    # TODO: apply action for update_indexes

    ne, de = len(new_indexes), len(delete_db_indexes)
    if ne > 0 or de > 0:
        logger.info(
            f'Applied for "{operation["collection_name"]}": {de} deleted, {ne} added'
        )
    return ne, de


def get_model_indexes(model) -> List:
    if hasattr(model.Config, "indexes"):
        return list(model.Config.indexes)
    return []


def get_all_indexes():
    """
    First imports all child models of Document since it's the abstract parent model.
    Then retrieve all the child modules and will try to get indexes inside the Config class.
    """
    operations = []
    for model in Document.__subclasses__():
        indexes = get_model_indexes(model)
        if indexes:
            collection_name = model._get_collection_name()
            obj = {
                "collection_name": collection_name,
                "create_indexes": indexes,
            }
            if (
                hasattr(model.Config, "allow_inheritance")
                and model.Config.allow_inheritance is True
            ):
                """If a model has child model"""
                if model.Config.index_inheritance_field is True:
                    """No _cls indexes will apply if index_inheritance_field = False"""
                    indexes.append(IndexModel([(INHERITANCE_FIELD_NAME, ASCENDING)]))
                for child_model in model.__subclasses__():
                    """Get all indexes that are defined in child model"""
                    indexes += get_model_indexes(child_model)
            operations.append(obj)
    return operations


def apply_indexes():
    """Run "python -m app.main apply-indexes" to apply and indexes."""

    """First get all indexes from all model."""
    operations = get_all_indexes()

    """Then execute each indexes operation for each model."""
    new_index, delete_index = 0, 0
    for operation in operations:
        ne, de = index_for_a_collection(operation)
        new_index += ne
        delete_index += de

    if delete_index:
        logger.info(f"{delete_index}, index deleted.")
    if new_index:
        logger.info(f"{new_index}, index created.")
    if [new_index, delete_index] == [0, 0]:
        logger.info("No change detected.")
