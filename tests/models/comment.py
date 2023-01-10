from datetime import datetime
from typing import List
from bson import ObjectId

from pydantic import BaseModel, Field

from mongodb_odm import PydanticObjectId
from mongodb_odm import ASCENDING, Document, IndexModel

MAX_CHILD_COMMENT = 100


class EmbeddedComment(BaseModel):
    user: PydanticObjectId = Field(...)
    description: str = Field(...)
    order: str = Field(default_factory=ObjectId)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Comment(Document):
    post: PydanticObjectId = Field(...)
    user: PydanticObjectId = Field(...)

    order: str = Field(default_factory=ObjectId)

    childs: List[EmbeddedComment] = []
    child_limit: int = Field(default=MAX_CHILD_COMMENT)

    description: str = Field(...)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "comment"
        indexes = [
            IndexModel([("post", ASCENDING)]),
        ]
