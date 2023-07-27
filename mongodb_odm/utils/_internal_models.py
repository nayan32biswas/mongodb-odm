from typing import Any, Optional, Set

from pydantic import BaseModel
from pymongo import MongoClient


class Connection(object):
    url: Optional[str] = None
    client: Optional[MongoClient[Any]] = None
    databases: Optional[Set[str]] = None


class RelationalFieldInfo(BaseModel):
    model: Any
    local_field: str
    related_field: Optional[str]


class CollectionConfig(BaseModel):
    collection_name: str
    child_collection_name: Optional[str] = None
    database_name: Optional[str] = None
