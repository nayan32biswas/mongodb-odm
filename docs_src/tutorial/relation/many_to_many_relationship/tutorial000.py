import os
from typing import Optional

from mongodb_odm import (
    ASCENDING,
    Document,
    Field,
    IndexModel,
    ODMObjectId,
    Relationship,
    apply_indexes,
    connect,
)


class Country(Document):
    name: str


class Skill(Document):
    name: str


class Player(Document):
    name: str
    country_id: ODMObjectId

    country: Optional[Country] = Relationship(local_field="country_id")

    class Config(Document.Config):
        indexes = [
            IndexModel([("country_id", ASCENDING)]),
        ]


class PlayerSkill(Document):
    player_id: ODMObjectId
    skill_id: ODMObjectId
    rating: int = Field(default=0, ge=1, le=100)

    player: Optional[Player] = Relationship(local_field="player_id")
    skill: Optional[Skill] = Relationship(local_field="skill_id")

    class Config(Document.Config):
        indexes = [
            IndexModel(
                [("player_id", ASCENDING), ("skill_id", ASCENDING)],
                unique=True,
            ),
        ]


def insert_data():
    brazil = Country(name="Brazil").create()
    argentina = Country(name="Argentina").create()
    france = Country(name="France").create()

    catching = Skill(name="Catching")
    running = Skill(name="Running")
    kicking = Skill(name="Kicking")

    pele = Player(name="Pelé", country_id=brazil.id).create()
    PlayerSkill(player_id=pele.id, skill_id=catching.id, rating=49).create()
    PlayerSkill(player_id=pele.id, skill_id=kicking.id, rating=49).create()

    maradona = Player(name="Diego Maradona", country_id=argentina.id).create()
    PlayerSkill(
        player_id=maradona.id, skill_id=catching.id, rating=48
    ).create()
    PlayerSkill(player_id=maradona.id, skill_id=kicking.id, rating=49).create()

    zidane = Player(name="Zinedine Zidane", country_id=france.id).create()
    PlayerSkill(player_id=zidane.id, skill_id=running.id, rating=42).create()
    PlayerSkill(player_id=zidane.id, skill_id=kicking.id, rating=42).create()


def read_data():
    pele = Player.get({"name": "Pelé"})
    skills = [p for p in PlayerSkill.find({"player_id": pele.id})]

    print(pele)
    print(skills)


def configuration():
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
    apply_indexes()


def main():
    configuration()
    insert_data()
    read_data()


if __name__ == "__main__":
    main()
