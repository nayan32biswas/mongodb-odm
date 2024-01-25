import os
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel, apply_indexes, connect


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None

    class ODMConfig(Document.ODMConfig):
        indexes = [
            IndexModel([("contact_email", ASCENDING)]),
        ]


def create_documents():
    Player(name="Pelé", country_code="BRA").create()
    Player(name="Diego Maradona", country_code="ARG", rating=97).create()


def main():
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
    apply_indexes()

    create_documents()


if __name__ == "__main__":
    main()
