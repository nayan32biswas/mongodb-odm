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
    player.delete()
