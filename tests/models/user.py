from datetime import datetime
from pydantic import Field
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel
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

    class Config:
        collection_name = "user"
        indexes = (
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel(
                [("email", ASCENDING)],
                unique=True,
                partialFilterExpression={"email": {"$type": "string"}},
            ),
        )


def get_user():
    USERNAME = "test-user"
    user = User.find_first({"username": "test-user"})
    if user:
        return user
    user = User(username=USERNAME, full_name="Full Name").create()
    return user
