import os
from typing import Optional  # (1)

from mongodb_odm import Document, connect  # (2)


class Player(Document):  # (3)
    name: str  # (4)
    country_code: str  # (5)
    rating: Optional[int] = None  # (6)


def create_documents():  # (11)
    Player(name="Pelé", country_code="BRA").create()  # (12)

    maradona = Player(
        name="Diego Maradona", country_code="ARG", rating=97
    ).create()  # (13)
    maradona = maradona.create()  # (14)

    Player(name="Zinedine Zidane", country_code="FRA", rating=96).create()


def main():  # (8)
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))  # (9)

    create_documents()  # (10)


if __name__ == "__main__":
    main()  # (7)
