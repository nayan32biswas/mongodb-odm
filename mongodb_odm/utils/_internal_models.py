from typing import Any, Optional, Set

from pydantic import BaseModel
from pymongo import MongoClient


class Connection:
    # Use this model to maintain database connection object structure.
    url: Optional[str] = None
    client: Optional[MongoClient[Any]] = None
    databases: Optional[Set[str]] = None


class RelationalFieldInfo(BaseModel):
    # We use this model to work with model relation field
    model: Any
    local_field: str
    related_field: Optional[str]


class CollectionConfig(BaseModel):
    # Connection configuration model for each model.
    collection_name: str
    child_collection_name: Optional[str] = None
    database_name: Optional[str] = None
