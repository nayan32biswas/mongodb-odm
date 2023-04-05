from typing import Any, Optional
from pydantic import BaseModel
from pymongo import MongoClient


class Connection(object):
    url: Optional[str] = None
    client: Optional[MongoClient[Any]] = None


class RelationalFieldInfo(BaseModel):
    model: Any
    local_field: str
    related_field: Optional[str]
