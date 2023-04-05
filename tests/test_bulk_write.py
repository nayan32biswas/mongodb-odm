import logging

from mongodb_odm import DeleteOne, Document, InsertOne, UpdateOne

from .conftest import init_config  # noqa

logger = logging.getLogger(__name__)


class NewModel(Document):
    title: str


def test_bulk_insert():
    NewModel.bulk_write(
        [
            InsertOne({"title": "bulk insert"}),
            InsertOne({"title": "bulk insert"}),
        ]
    )


def test_bulk_update():
    NewModel.bulk_write(
        [
            UpdateOne(
                {"title": "bulk insert"}, {"$set": {"title": "updated"}}
            ),
        ]
    )


def test_bulk_delete():
    NewModel.bulk_write(
        [DeleteOne({"title": "bulk insert"}), DeleteOne({"title": "updated"})]
    )
