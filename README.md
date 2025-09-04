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

The purpose of this module is to provide easy access to the database with the python object feature with **MongoDB** and **PyMongo**. With PyMongo that was very easy to make spelling mistakes in a collection name when you are doing database operation. This module provides you with minimal ODM with a modeling feature so that you don’t have to look up the MongoDB dashboard(Mongo Compass) to know about field names or data types.

**MongoDB-ODM** is based on Python type annotations, and powered by <a href="https://pymongo.readthedocs.io/en/stable/" class="external-link" target="_blank">PyMongo</a> and <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>.

The key features are:

- **Intuitive to write**: Great editor support. Completion everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
- **Easy to use**: It has sensible defaults and does a lot of work underneath to simplify the code you write.
- **Compatible**: It is designed to be compatible with **FastAPI**, **Pydantic**, and **PyMongo**.
- **Extensible**: You have all the power of **PyMongo** and **Pydantic** underneath.
- **Short**: Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in **PyMongo** and Pydantic.

---

## Requirements

**MongoDB-ODM** will work on <a href="https://www.python.org/downloads" class="external-link" target="_blank">Python 3.9 and above</a>.

**MongoDB-ODM** is built on top of **PyMongo** and **Pydantic**. These packages are required and will be auto-installed when **MongoDB-ODM** is installed.

## Installation

```console
$ pip install mongodb-odm
```

## Example

### Define model

```Python
import os
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel, connect


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None

    class ODMConfig(Document.ODMConfig):
        indexes = [
            IndexModel([("rating", ASCENDING)]),
        ]
```

### Set Connection

```Python
connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
```

### Create Document

```Python
pele = Player(name="Pelé", country_code="BRA").create()
maradona = Player(name="Diego Maradona", country_code="ARG", rating=97).create()
zidane = Player(name="Zinedine Zidane", country_code="FRA", rating=96).create()
```

### Retrieve Document

#### Find data from collection

```Python
for player in Player.find():
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
import os
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel, connect


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None

    class ODMConfig(Document.ODMConfig):
        indexes = [
            IndexModel([("rating", ASCENDING)]),
        ]
```

- To create indexes in the database, declare an <a href="https://pymongo.readthedocs.io/en/stable/tutorial.html#indexing" class="external-link" target="_blank">IndexModel</a> and assign it to the indexes array in the ODMConfig class. **IndexModel** modules are directly imported from **PyMongo**.
- Import `apply_indexes` from `mongodb_odm`. Call the `apply_indexes` function from your CLI. You can use <a href="https://typer.tiangolo.com" class="external-link" target="_blank">Typer</a> to implement a CLI.

## Example Code

This is the example of full code of above.

```python
import os
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel, connect


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None

    class ODMConfig(Document.ODMConfig):
        indexes = [
            IndexModel([("rating", ASCENDING)]),
        ]


connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))

pele = Player(name="Pelé", country_code="BRA").create()
maradona = Player(name="Diego Maradona", country_code="ARG", rating=97).create()
zidane = Player(name="Zinedine Zidane", country_code="FRA", rating=96).create()

for player in Player.find():
    print(player)

player = Player.find_one({"name": "Pelé"})
if player:
    player.rating = 98  # potential
    player.update()

player = Player.find_one({"name": "Pelé"})
if player:
    player.delete()  # RIP
```

### Supported Framework

**MongoDB-ODM** is not framework-dependent. You can use this package in any system. However, we take special consideration to be compatible with <a href="https://fastapi.tiangolo.com/" class="external-link" target="_blank">FastAPI</a> and <a href="https://flask.palletsprojects.com/en/2.2.x/" class="external-link" target="_blank">Flask</a>.

### Credit

This package is built on top of <a href="https://pymongo.readthedocs.io/en/stable" class="external-link" target="_blank">PyMongo</a> and <a href="https://docs.pydantic.dev" class="external-link" target="_blank">Pydantic</a>.

Documentation generated by <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a> and <a href="https://squidfunk.github.io/mkdocs-material/" class="external-link" target="_blank">Material for MkDocs</a>.

Documentation inspired by <a href="https://sqlmodel.tiangolo.com" class="external-link" target="_blank">SQLModel</a>.

However, we use other packages for development and other purposes. Check **pyproject.toml** to learn about all packages we use to build this package.

## License

This project is licensed under the terms of the [MIT license](https://github.com/nayan32biswas/mongodb-odm/blob/main/LICENSE).
