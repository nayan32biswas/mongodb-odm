import os
from typing import Optional  # (1)

from mongodb_odm import ASCENDING, Document, IndexModel, apply_indexes, connect  # (2)


class Player(Document):  # (3)
    name: str  # (4)
    country_code: str  # (5)
    rating: Optional[int] = None  # (6)

    class Config(Document.Config):  # (7)
        indexes = [  # (8)
            IndexModel([("rating", ASCENDING)]),
        ]


def create_players():  # (14)
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


def read_players():  # (16)
    players = Player.find()  # (17)
    for player in players:  # (18)
        print(player)


def filter_players():  # (20)
    players = Player.find(filter={"rating": {"$gte": 90}})  # (21)
    for player in players:  # (22)
        print(player)


def find_one_object():  # (24)
    player = Player.find_one({"rating": {"country_code": "BRA", "$gte": 90}})  # (25)
    if player:
        print(player)


def get_object():  # (27)
    player = Player.find_one({"name": "Pelé"})  # (28)
    print(player)


def get_or_create_object():  # (30)
    player = Player.get_or_create({"name": "Pelé"})  # (31)
    print(player)


def count_total_documents():  # (33)
    count = Player.count_documents({"name": "Pelé"})  # (34)
    print(count)


def check_exists():  # (36)
    is_exists = Player.exists({"name": "Pelé"})  # (37)
    print(is_exists)


def aggregate_collection():  # (39)
    pipeline = [{"$match": {"rating": {"$gte": 90}}}]  # (40)
    data_list = Player.aggregate(pipeline)  # (41)
    for data in data_list:  # (42)
        print(data)


def get_random_one():  # (44)
    player = Player.get_random_one({"rating": {"$gte": 90}})  # (45)
    print(player)


def main():  # (10)
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))  # (11)
    apply_indexes()  # (12)
    create_players()  # (13)

    read_players()  # (15)
    filter_players()  # (19)
    find_one_object()  # (23)
    get_object()  # (26)
    get_or_create_object()  # (29)
    count_total_documents()  # (32)
    check_exists()  # (35)
    aggregate_collection()  # (38)
    get_random_one()  # (43)


if __name__ == "__main__":
    main()  # (9)
