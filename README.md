# MongoDB-ODM

<p align="center">
    <em>MongoDB-ODM, NOSQL databases in Python, designed for simplicity, compatibility, and robustness.</em>
</p>

<p align="center">

<a href="https://github.com/nayan32biswas/mongodb-odm" target="_blank">
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/nayan32biswas/mongodb-odm/total?color=success">
</a>
<a href="https://pypi.org/project/mongodb-odm/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/mongodb-odm?color=blue">
</a>
</p>

---

## Introduction

The purpose of this module is to do provide easy access to the database with the python object feature with MongoDB and pymongo. With pymongo that was very easy to make spelling mistakes of a collection name when you are doing database operation. This module provides you minimal ODM with a modeling feature so that you don’t have to look up the MongoDB dashboard(Mongo Compass) to know about field names or data types.

**MongoDb-ODM** is based on Python type annotations, and powered by <a href="https://pymongo.readthedocs.io/en/stable/" class="external-link" target="_blank">PyMongo</a> and <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>.

The key features are:

- **Intuitive to write**: Great editor support. Completion everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
- **Easy to use**: It has sensible defaults and does a lot of work underneath to simplify the code you write.
- **Compatible**: It is designed to be compatible with **FastAPI**, **Pydantic**, and **PyMongo**.
- **Extensible**: You have all the power of **PyMongo** and **Pydantic** underneath.
- **Short**: Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in **PyMongo** and Pydantic.

---

## Requirement

**MongoDb-ODM** will work on <a href="https://www.python.org/downloads/" class="external-link" target="_blank">Python 3.7 and above</a>

This **MongoDb-ODM** is build top of **PyMongo** and **Pydantic**. Those package are required and will auto install while **MongoDb-ODM** was installed.

## Installation

```console
$ pip install mongodb-odm
```

## Example

### Define model

```py
from datetime import datetime
from pydantic import Field
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel


class User(Document):
    username: str = Field(...)
    full_name: str = Field(...)

    last_login: datetime = Field(default_factory=datetime.utcnow)
    password: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "user"
        indexes = (
            IndexModel([("username", ASCENDING)], unique=True),
        )
```

### Create Document

```py
user = User(
    username="username",
    full_name="Example Name",
    password="hash-password",
).create()
```

### Retrieve Document

- Filter data from collection

```py
for user in User.find():
    print(user)
```

- Find first object with filter

```py
user = User.find_first()
```

### Update Data


```py
user = User.find_first()
if user:
    user.full_name = "New Name"
    user.update()
```

### Delete Data

```py
user = User.find_first()
if user:
    user.delete()
```

### Apply Indexes

```py
from mongodb_odm import apply_indexes, ASCENDING, Document, IndexModel


class User(Document):
    ...

    class Config:
        indexes = (
            IndexModel([("username", ASCENDING)], unique=True),
        )
```

- To create indexes in database declare [IndexModel](https://pymongo.readthedocs.io/en/stable/tutorial.html#indexing) and assign in indexes array in Config class. **IndexModel** module that are directly imported from **pymongo**.
- Call `apply_indexes` function from your CLI. You can use [Typer](https://typer.tiangolo.com/) to implement CLI.
