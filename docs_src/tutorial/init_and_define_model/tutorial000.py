from typing import Optional

from mongodb_odm import Document


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None

    class Config(Document.Config):
        collection_name = "player"
