# ODM

<p align="center">
    <em>MongoDB-ODM, NOSQL databases in Python, designed for simplicity, compatibility, and robustness.</em>
</p>

<p align="center">

<a href="https://github.com/nayan32biswas/mongodb-odm" target="_blank">
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/nayan32biswas/mongodb-odm/total?color=%2300FF00&logo=github&style=flat-square">
</a>
<a href="https://pypi.org/project/mongodb-odm/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/mongodb-odm?color=%2300FF00&label=PyPi%20Package&logo=pypi">
</a>
</p>

---

## Introduction

The purpose of this module is to do provide easy access to the database with the python object feature with MongoDB and pymongo. With pymongo that was very easy to make spelling mistakes of a collection name when you are doing database operation. This module provides you minimal ODM with a modeling feature so that you don’t have to look up the MongoDB dashboard(Mongo Compass) to know about field names or data types.

**MongoDb-ODM** is based on Python type annotations, and powered by <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> and <a href="https://pymongo.readthedocs.io/en/stable/" class="external-link" target="_blank">PyMongo</a>.

The key features are:

- **Intuitive to write**: Great editor support. Completion everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
- **Easy to use**: It has sensible defaults and does a lot of work underneath to simplify the code you write.
- **Compatible**: It is designed to be compatible with **FastAPI**, **Pydantic**, and **PyMongo**.
- **Extensible**: You have all the power of **PyMongo** and Pydantic underneath.
- **Short**: Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in **PyMongo** and Pydantic.

---

## Requirement

**MongoDb-ODM** will work on <a href="https://www.python.org/downloads/" class="external-link" target="_blank">Python 3.6 and above</a>

This **MongoDb-ODM** is build top of **PyMongo** and **Pydantic**. Those package are required and will auto install while **MongoDb-ODM** was installed.

## Example

#### Define model

```py
from datetime import datetime
from pydantic import Field
from pymongo import IndexModel, ASCENDING
from typing import Optional

from mongodb_odm.models import Document


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
            IndexModel([("email", ASCENDING)]),
        )

```

#### Create Document

```py
user = User(
    email="example@example.com",
    full_name="Example Name",
    password="hash-password",
).create()
```

#### Retrive Document

- Filter data from collection

```py
for user in find({"is_active": True}):
    print(user)

```

- Find first object with filter

```py
user = User.find_first({"is_active": True})

```

#### Update Data


```py
user = User.find_first({"is_active": True})
user.full_name = "New Name"

```

#### Delete Data

```py
user = User.find_first({"is_active": True})
if user:
    user.delete()
```
