import os
from typing import Optional

from mongodb_odm import ASCENDING, Document, IndexModel, apply_indexes, connect
from pymongo import MongoClient


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


def filter_documents():
    players = Player.find_raw(filter={Player.rating: {"$gte": 10}})
    for player in players:
        print(player)
    print()


def pymongo_find_and_find_raw_comparison():
    filter = {Player.rating: {"$gte": 10}}

    connection_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb")
    db = MongoClient(connection_url).get_database()

    py_players = db.player.find(filter)
    odm_players = Player.find_raw(filter)

    print(py_players, odm_players)


def main():
    configuration()
    create_players()

    filter_documents()
    pymongo_find_and_find_raw_comparison()


if __name__ == "__main__":
    main()
