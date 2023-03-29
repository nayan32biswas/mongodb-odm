import os
from typing import Optional

from mongodb_odm import (
    ASCENDING,
    Document,
    IndexModel,
    ODMObjectId,
    Relationship,
    apply_indexes,
    connect,
)


class Country(Document):
    name: str


class Player(Document):
    name: str
    country_id: ODMObjectId
    rating: Optional[int] = None

    country: Optional[Country] = Relationship(local_field="country_id")

    class Config(Document.Config):
        indexes = [
            IndexModel([("country_id", ASCENDING)]),
        ]


def configuration():
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
    apply_indexes()


def insert_data():
    bangladesh = Country(name="Bangladesh").create()

    Player(name="Jamal Bhuyan", country_id=bangladesh.id).create()
    Player(name="Mohamed Emon Mahmud", country_id=bangladesh.id).create()


def read_data():
    for player in Player.find():
        print(player)
    print()


def read_data_with_related_field():
    player_qs = Player.find()
    for player in Player.load_related(player_qs):
        print(player)
    print()


def read_related_data_of_specific_field():
    player_qs = Player.find()
    for player in Player.load_related(player_qs, fields=["country"]):
        print(player)
    print()


def read_related_data_for_single_obj():
    """Load related data in naive way"""
    player = Player.find_one()
    if player:
        player.country = Country.find_one({"_id": player.country_id})
    print(player)

    """Load related data with load_related"""
    player = Player.find_one()
    if player:
        player = Player.load_related([player])[0]
    print(player)


def main():
    configuration()
    insert_data()

    read_data()
    read_data_with_related_field()
    read_related_data_of_specific_field()
    read_related_data_for_single_obj()


if __name__ == "__main__":
    main()
