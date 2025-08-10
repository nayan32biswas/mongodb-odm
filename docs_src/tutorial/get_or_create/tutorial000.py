import os
from typing import Any, Optional

from mongodb_odm import ASCENDING, Document, IndexModel, apply_indexes, connect


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None

    class ODMConfig(Document.ODMConfig):
        indexes = [
            IndexModel([("rating", ASCENDING)]),
        ]


def create_players():
    Player(name="Pelé", country_code="BRA", rating=98).create()
    Player(name="Diego Maradona", country_code="ARG", rating=97).create()
    Player(name="Zinedine Zidane", country_code="FRA", rating=94).create()
    Player(name="Ronaldo", country_code="BRA", rating=94).create()
    Player(name="Neymar", country_code="BRA", rating=89).create()
    Player(name="Lionel Messi", country_code="ARG", rating=91).create()
    Player(name="Ángel Di María", country_code="ARG", rating=84).create()
    Player(name="Karim Benzema", country_code="FRA", rating=89).create()
    Player(name="Antoine Griezmann", country_code="FRA", rating=85).create()
    Player(name="Kylian Mbappé", country_code="FRA", rating=91).create()
    Player(name="Gerd Müller", country_code="GER").create()
    Player(name="Miroslav Klose", country_code="GER", rating=91).create()
    Player(name="Thomas Müller", country_code="GER", rating=87).create()
    Player(name="Cristiano Ronaldo", country_code="POR", rating=87).create()
    Player(name="Eusébio", country_code="POR", rating=93).create()
    Player(name="Diogo Jota", country_code="POR", rating=85).create()
    Player(name="David Beckham", country_code="ENG", rating=89).create()
    Player(name="Wayne Rooney", country_code="ENG", rating=80).create()
    Player(name="Harry Kane", country_code="ENG", rating=89).create()


def configuration():
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
    apply_indexes()


def general_process():
    filter: dict[str, Any] = {"name": "Pelé", "country_code": "example@test.com"}
    player = Player.find_one(filter)
    created = False
    if not player:
        player = Player(**filter).create()
        created = True
    print(created, player)


def get_or_create_document():
    player, created = Player.get_or_create(
        filter={"name": "Pelé", "country_code": "BRA"}
    )
    print(created, player)

    player, created = Player.get_or_create(
        filter={"name": "Vini Jr.", "country_code": "BRA"}
    )
    print(created, player)


def main():
    configuration()

    general_process()
    create_players()

    general_process()
    get_or_create_document()


if __name__ == "__main__":
    main()
