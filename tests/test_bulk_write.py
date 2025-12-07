import pytest
from mongodb_odm import DeleteOne, Document, InsertOne, UpdateOne

from tests.conftest import INIT_CONFIG


class NewModel(Document):
    title: str


@pytest.mark.usefixtures(INIT_CONFIG)
def test_bulk_insert():
    NewModel.bulk_write(
        [
            InsertOne({NewModel.title: "bulk insert"}),
            InsertOne({NewModel.title: "bulk insert"}),
        ]
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_bulk_update():
    NewModel.bulk_write(
        [
            UpdateOne(
                {NewModel.title: "bulk insert"},
                {"$set": {NewModel.title: "updated"}},
            ),
        ]
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_bulk_delete():
    NewModel.bulk_write(
        [
            DeleteOne({NewModel.title: "bulk insert"}),
            DeleteOne({NewModel.title: "updated"}),
        ]
    )
