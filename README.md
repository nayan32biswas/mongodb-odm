# ODM

## Introduction

The purpose of this module is to do provide easy access to the database with the python object feature with MongoDB and pymongo. With pymongo that was very easy to make spelling mistakes of a collection name when you are doing database operation. This module provides you minimal ODM with a modeling feature so that you don’t have to look up the MongoDB dashboard(Mongo Compass) to know about field names or data types.

## Requirement

Since this module is build top of pymongo and pydantic it's good have knowledge about those packages.

## Example models

```py
from datetime import datetime
from pymongo import ASCENDING, IndexModel
from pydantic import EmailStr, Field
from typing import Optional

from app.odm.models import Document


class User(Document):
    email: EmailStr = Field(...)
    name: Optional[str] = Field(default=None)
    photo_link: str = Field(default=None)

    password: Optional[str] = Field(default=None)
    last_login: datetime = Field(default_factory=datetime.utcnow)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "user"
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True),
        ]
```

## Creation

To create an object and call create method. Create method accept one boolean optional argument `get_obj`. If you want to pull full data and assign to the existing model then call `obj.create(get_obj=True)` It will recall database with returnd id and update value of existing model.

```py
user = User(
    email="demo@example.com",
    name="Example",
    password="hash-password"
)
user.create()
```

## Retrive Data

```py
users = User.find()
for user in users:
    print(user)
```

To retrive data there is a function call **find**. It's return python Iterator. Unless you accessing the value the function will not execute any DB call.


Paramiter of **find**.
