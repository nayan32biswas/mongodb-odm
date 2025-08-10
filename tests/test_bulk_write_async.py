import pytest
from mongodb_odm import DeleteOne, Document, InsertOne, UpdateOne

from tests.conftest import ASYNC_INIT_CONFIG


class NewModel(Document):
    title: str


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_bulk_insert():
    await NewModel.abulk_write(
        [
            InsertOne({"title": "bulk insert"}),
            InsertOne({"title": "bulk insert"}),
        ]
    )


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_bulk_update():
    await NewModel.abulk_write(
        [
            UpdateOne({"title": "bulk insert"}, {"$set": {"title": "updated"}}),
        ]
    )


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_bulk_delete():
    await NewModel.abulk_write(
        [DeleteOne({"title": "bulk insert"}), DeleteOne({"title": "updated"})]
    )
