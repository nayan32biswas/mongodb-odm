# MongoDB-ODM

<p align="center">
    <em>MongoDB-ODM, NOSQL databases in Python, designed for simplicity, compatibility, and robustness.</em>
</p>

<p align="center">

<a href="https://github.com/nayan32biswas/mongodb-odm/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/nayan32biswas/mongodb-odm/actions/workflows/test.yml/badge.svg?branch=main&event=push" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/nayan32biswas/mongodb-odm" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/nayan32biswas/mongodb-odm.svg" alt="Coverage">
<br />
<a href="https://pypi.org/project/mongodb-odm/" target="_blank">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/mongodb-odm?color=%2334D058&label=PyPi%20Package">
</a>
<a href="https://pypi.org/project/mongodb-odm/" target="_blank">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/mongodb-odm?color=%2334D058">
</a>

</p>

---

**Documentation**: <a href="https://mongodb-odm.readthedocs.io" target="_blank">https://mongodb-odm.readthedocs.io</a>

**PyPi**: <a href="https://pypi.org/project/mongodb-odm" target="_blank">https://pypi.org/project/mongodb-odm</a>

**Repository**: <a href="https://github.com/nayan32biswas/mongodb-odm" target="_blank">https://github.com/nayan32biswas/mongodb-odm</a>

---

## Introduction

The purpose of this module is to provide easy access to the database with the python object feature with MongoDB and pymongo. With pymongo that was very easy to make spelling mistakes in a collection name when you are doing database operation. This module provides you with minimal ODM with a modeling feature so that you don’t have to look up the MongoDB dashboard(Mongo Compass) to know about field names or data types.

**MongoDB-ODM** is based on Python type annotations, and powered by <a href="https://pymongo.readthedocs.io/en/stable/" class="external-link" target="_blank">PyMongo</a> and <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>.

The key features are:

- **Intuitive to write**: Great editor support. Completion everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
- **Easy to use**: It has sensible defaults and does a lot of work underneath to simplify the code you write.
- **Compatible**: It is designed to be compatible with **FastAPI**, **Pydantic**, and **PyMongo**.
- **Extensible**: You have all the power of **PyMongo** and **Pydantic** underneath.
- **Short**: Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in **PyMongo** and Pydantic.

---

## Requirement

**MongoDB-ODM** will work on <a href="https://www.python.org/downloads/" class="external-link" target="_blank">Python 3.8 and above</a>

This **MongoDB-ODM** is built on top of **PyMongo** and **Pydantic**. Those packages are required and will auto-install while **MongoDB-ODM** was installed.

## Installation

```console
$ pip install mongodb-odm
```

## Example

### Define model

```Python
from typing import Optional
from mongodb_odm import connect, Document, Field, IndexModel, ASCENDING


class Player(Document):
    name: str = Field(...)
    country: Optional[str] = None

    class Config(Document.Config):
        collection_name = "player"
        indexes = [
            IndexModel([("country", ASCENDING)]),
        ]
```

### Set Connection

```Python
connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
```

### Create Document

```Python
pele = Player(name="Pelé", country_code="BRA").create()
maradona = Player(
    name="Diego Maradona", country_code="ARG", rating=97
).create()
zidane = Player(name="Zinedine Zidane", country_code="FRA", rating=96).create()
```

### Retrieve Document

#### Find data from collection

```Python
for player in Player.find({"name": "ARG"}):
    print(player)
```

#### Find one object with filter

```Python
player = Player.find_one({"name": "Pelé"})
```

### Update Data

```Python
player = Player.find_one({"name": "Pelé"})
if player:
    player.rating = 98  # potential
    player.update()
```

### Delete Data

```Python
player = Player.find_one({"name": "Pelé"})
if player:
    player.delete()
```

### Apply Indexes

```Python
from mongodb_odm import Document, IndexModel, ASCENDING


class Player(Document):
    ...
    class Config(Document.Config):
        indexes = [
            IndexModel([("country", ASCENDING)]),
        ]
```

- To create indexes in the database declare [IndexModel](https://pymongo.readthedocs.io/en/stable/tutorial.html#indexing) and assign in indexes array in Config class. **IndexModel** modules that are directly imported from **pymongo**.
- Call the `apply_indexes` function from your CLI. You can use [Typer](https://typer.tiangolo.com/) to implement CLI.

## Example Code

This is a short example of full code

```python
import os
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel, connect


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None

    class Config(Document.Config):
        indexes = [
            IndexModel([("rating", ASCENDING)]),
        ]


connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))

pele = Player(name="Pelé", country_code="BRA").create()
maradona = Player(
    name="Diego Maradona", country_code="ARG", rating=97
).create()
zidane = Player(name="Zinedine Zidane", country_code="FRA", rating=96).create()

for player in Player.find():
    print(player)

player = Player.find_one({"name": "Pelé"})
if player:
    player.rating = 98  # potential
    player.update()

player = Player.find_one({"name": "Pelé"})
```

### Supported Framework

**MongoDB-ODM** is not framework dependent. We can use this package in any system. But we take special consideration being compatible with <a href="https://fastapi.tiangolo.com/" class="external-link" target="_blank">FastAPI</a> and <a href="https://flask.palletsprojects.com/en/2.2.x/" class="external-link" target="_blank">Flask</a>.

### Credit

This package is built on top of <a href="https://pymongo.readthedocs.io/en/stable" class="external-link" target="_blank">PyMongo</a> and <a href="https://docs.pydantic.dev" class="external-link" target="_blank">Pydantic</a>.

Documentation generated by <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a> and <a href="https://squidfunk.github.io/mkdocs-material/" class="external-link" target="_blank">Material for MkDocs</a>.

Documentation inspired by <a href="https://sqlmodel.tiangolo.com" class="external-link" target="_blank">SQLModel</a>.

But we use other packages for development and other purposes. Check **pyproject.toml** to know about all packages we use to build this package.

## License

This project is licensed under the terms of the [MIT license](https://github.com/nayan32biswas/mongodb-odm/blob/main/LICENSE).
