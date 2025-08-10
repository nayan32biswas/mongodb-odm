import os
from typing import Optional

from mongodb_odm import (
    ASCENDING,
    BaseModel,
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


class EmbeddedSkill(BaseModel):
    skill_id: ODMObjectId
    rating: int = Field(default=0, ge=1, le=100)


class Player(Document):
    name: str
    country_id: ODMObjectId
    skills: list[EmbeddedSkill] = []

    country: Optional[Country] = Relationship(local_field="country_id")

    class ODMConfig(Document.ODMConfig):
        indexes = [
            IndexModel([("country_id", ASCENDING)]),
        ]


def insert_data():
    brazil = Country(name="Brazil").create()
    argentina = Country(name="Argentina").create()
    france = Country(name="France").create()

    catching = Skill(name="Catching")
    running = Skill(name="Running")
    kicking = Skill(name="Kicking")

    Player(
        name="Pelé",
        country_id=brazil.id,
        skills=[
            EmbeddedSkill(skill_id=catching.id, rating=49),
            EmbeddedSkill(skill_id=kicking.id, rating=49),
        ],
    ).create()
    Player(
        name="Diego Maradona",
        country_id=argentina.id,
        skills=[
            EmbeddedSkill(skill_id=catching.id, rating=48),
            EmbeddedSkill(skill_id=kicking.id, rating=49),
        ],
    ).create()
    Player(
        name="Zinedine Zidane",
        country_id=france.id,
        skills=[
            EmbeddedSkill(skill_id=running.id, rating=42),
            EmbeddedSkill(skill_id=kicking.id, rating=42),
        ],
    ).create()


def read_data():
    pele = Player.get({"name": "Pelé"})
    print(pele)


def configuration():
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
    apply_indexes()


def main():
    configuration()
    insert_data()
    read_data()


if __name__ == "__main__":
    main()
