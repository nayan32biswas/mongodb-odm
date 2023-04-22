import os
from typing import Optional

from mongodb_odm import Document, connect


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None


def create_documents():
    pele = Player(name="Pelé", country_code="BRA").create()

    with Document.start_session() as session:
        with session.start_transaction():
            pele.rating = 98
            pele.update(session=session)

            maradona = Player(name="Diego Maradona", country_code="ARG", rating=97)
            maradona.create(session=session)


def main():
    connect(os.environ.get("REMOTE_MONGO_URL", "mongodb://localhost:27017/testdb"))

    create_documents()


if __name__ == "__main__":
    main()
