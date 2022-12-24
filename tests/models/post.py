from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field
from pymongo import ASCENDING, IndexModel

from mongodb_odm import PydanticObjectId
from mongodb_odm import Document


class Post(Document):
    author: PydanticObjectId = Field(...)

    title: str = Field(max_length=255)
    short_description: Optional[str] = Field(max_length=512, default=None)
    cover_image: Optional[str] = None

    published_at: Optional[datetime] = None
    is_publish: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        indexes = [
            IndexModel([("author", ASCENDING)]),
        ]


class Content(Document):
    post: PydanticObjectId = Field(...)
    order: Optional[int] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "content"
        allow_inheritance = True
        indexes = [
            IndexModel([("post", ASCENDING), ("order", ASCENDING)]),
        ]


class ContentDescription(Content):
    description: str = Field(...)


class ImageStyle(str, Enum):
    CENTER = "CENTER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ORDER = "ORDER"
    CAROUSEL = "CAROUSEL"


class ContentImage(Content):
    style: ImageStyle = Field(default=ImageStyle.CENTER)
    image_path: str = Field(...)
