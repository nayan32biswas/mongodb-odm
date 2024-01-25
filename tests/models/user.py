from datetime import datetime
from typing import Optional

from mongodb_odm import ASCENDING, Document, Field, IndexModel

from ..conftest import init_config  # noqa


class User(Document):
    username: str = Field(...)
    email: Optional[str] = Field(default=None)
    full_name: str = Field(...)

    is_active: bool = True
    date_joined: datetime = Field(default_factory=datetime.utcnow)

    last_login: datetime = Field(default_factory=datetime.utcnow)
    password: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class ODMConfig(Document.ODMConfig):
        collection_name = "user"
        indexes = [
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel(
                [("email", ASCENDING)],
                unique=True,
                partialFilterExpression={"email": {"$type": "string"}},
            ),
        ]


def get_user():
    user = User.find_one({"username": "one"})
    if user:
        return user
    user = User(username="one", full_name="Full Name").create()
    return user
