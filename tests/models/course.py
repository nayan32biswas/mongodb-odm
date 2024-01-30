from datetime import datetime
from enum import Enum
from typing import List, Optional

from mongodb_odm import (
    ASCENDING,
    TEXT,
    BaseModel,
    Document,
    Field,
    IndexModel,
    ODMObjectId,
    Relationship,
)

from .user import User


class Course(Document):
    author_id: ODMObjectId = Field(...)

    title: str = Field(max_length=255)
    short_description: Optional[str] = Field(max_length=512, default=None)
    cover_image: Optional[str] = None

    publish_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    author: Optional[User] = Relationship(local_field="author_id")

    class ODMConfig(Document.ODMConfig):
        indexes = [
            IndexModel([("author_id", ASCENDING)]),
            IndexModel([("title", TEXT), ("short_description", TEXT)]),
        ]


class Content(Document):
    course_id: ODMObjectId = Field(...)
    order: Optional[int] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    course: Optional[Course] = Relationship(local_field="course_id")

    class ODMConfig(Document.ODMConfig):
        collection_name = "content"
        allow_inheritance = True
        indexes = [
            IndexModel([("course_id", ASCENDING), ("order", ASCENDING)]),
        ]


class ContentDescription(Content):
    description: str = Field(...)

    class ODMConfig(Document.ODMConfig):
        allow_inheritance = False


class ImageStyle(str, Enum):
    CENTER = "CENTER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ORDER = "ORDER"
    CAROUSEL = "CAROUSEL"


class ContentImage(Content):
    style: ImageStyle = Field(default=ImageStyle.CENTER)
    image_path: str = Field(...)

    class ODMConfig(Document.ODMConfig):
        allow_inheritance = False


class EmbeddedComment(BaseModel):
    user_id: ODMObjectId = Field(...)
    description: str = Field(...)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Comment(Document):
    course_id: ODMObjectId = Field(...)
    user_id: ODMObjectId = Field(...)

    children: List[EmbeddedComment] = []
    description: str = Field(...)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    course: Optional[Course] = Relationship(local_field="course_id")
    user: Optional[User] = Relationship(local_field="user_id")

    class ODMConfig(Document.ODMConfig):
        collection_name = "comment"
        indexes = [
            IndexModel([("course_id", ASCENDING)]),
        ]
