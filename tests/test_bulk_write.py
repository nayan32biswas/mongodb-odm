import pytest
from mongodb_odm import DeleteOne, Document, InsertOne, UpdateOne

from tests.conftest import INIT_CONFIG


class NewModel(Document):
    title: str


@pytest.mark.usefixtures(INIT_CONFIG)
def test_bulk_insert():
    NewModel.bulk_write(
        [
            InsertOne({"title": "bulk insert"}),
            InsertOne({"title": "bulk insert"}),
        ]
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_bulk_update():
    NewModel.bulk_write(
        [
            UpdateOne({"title": "bulk insert"}, {"$set": {"title": "updated"}}),
        ]
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_bulk_delete():
    NewModel.bulk_write(
        [DeleteOne({"title": "bulk insert"}), DeleteOne({"title": "updated"})]
    )
