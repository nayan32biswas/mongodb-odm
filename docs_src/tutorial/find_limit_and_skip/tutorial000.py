import os
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel, apply_indexes, connect


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None

    class ODMConfig(Document.ODMConfig):
        indexes = [
            IndexModel([("rating", ASCENDING)]),
        ]


def configuration():
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
    apply_indexes()


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


def limit_data():
    players = Player.find(limit=2)
    for player in players:
        print(player)
    print()


def skip_data():
    players = Player.find(skip=2)
    for player in players:
        print(player)
    print()


def skip_and_limit_data():
    players = Player.find(skip=3, limit=2)
    for player in players:
        print(player)
    print()


def implement_pagination(page, limit):
    skip = (page - 1) * limit
    filter = {Player.rating: {"$gte": 90}}
    players = Player.find(filter=filter, skip=skip, limit=limit)
    for player in players:
        print(player)
    print()


def main():
    configuration()
    create_players()

    limit_data()
    skip_data()
    skip_and_limit_data()
    implement_pagination(page=1, limit=10)


if __name__ == "__main__":
    main()
