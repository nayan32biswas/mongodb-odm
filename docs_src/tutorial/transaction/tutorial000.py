import os
from typing import Optional

from mongodb_odm import Document, connect
from pymongo.errors import OperationFailure


class Player(Document):
    name: str
    country_code: str
    rating: Optional[int] = None


def create_documents():
    with Document.start_session() as session:
        with session.start_transaction():
            try:
                Player(
                    name="Pelé",
                    country_code="BRA",
                ).create(session=session)

                maradona = Player(name="Diego Maradona", country_code="ARG")
                maradona.create(session=session)
            except OperationFailure:
                session.abort_transaction()


def update_documents():
    with Document.start_session() as session:
        with session.start_transaction():
            try:
                pele = Player.get({"name": "Pelé"})
                pele.rating = 98
                pele.update(session=session)

                maradona = Player.get({"name": "Diego Maradona"})
                pele.rating = 97
                maradona.update(session=session)
            except OperationFailure:
                session.abort_transaction()


def delete_documents():
    with Document.start_session() as session:
        with session.start_transaction():
            try:
                pele = Player.get({"name": "Pelé"})
                pele.delete(session=session)

                maradona = Player.get({"name": "Diego Maradona"})
                maradona.delete(session=session)
            except OperationFailure:
                session.abort_transaction()


def main():
    # Use a database that has a replica set.
    connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))

    create_documents()
    update_documents()
    delete_documents()


if __name__ == "__main__":
    main()
