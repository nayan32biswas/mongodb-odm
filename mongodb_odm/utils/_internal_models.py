from typing import Any, Optional, Set

from pydantic import BaseModel
from pydantic._internal._repr import Representation as PydanticRepresentation
from pymongo import MongoClient


class Connection:
    # Use this model to maintain database connection object structure.
    url: Optional[str] = None
    client: Optional[MongoClient[Any]] = None
    databases: Optional[Set[str]] = None


class RelationalFieldInfo(PydanticRepresentation):
    def __init__(
        self, *, model: Any, local_field: str, related_field: Optional[str] = None
    ) -> None:
        self.model = model
        self.local_field = local_field
        self.related_field = related_field


class CollectionConfig(BaseModel):
    # Connection configuration model for each model.
    collection_name: str
    child_collection_name: Optional[str] = None
    database_name: Optional[str] = None
    has_children: bool = False
