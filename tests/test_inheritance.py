import logging

from bson import ObjectId

from .conftest import init_config  # noqa
from .models.course import Content, ContentDescription, Course
from .utils import populate_data

logger = logging.getLogger(__name__)


def test_parent_data_retrieve():
    populate_data()
    for obj in Content.find():
        assert isinstance(obj._id, ObjectId)


def test_child_data_retrieve():
    populate_data()
    for obj in ContentDescription.find():
        assert isinstance(obj._id, ObjectId)


def test_child_count():
    populate_data()
    count = ContentDescription.count_documents()
    assert isinstance(count, int)


def test_child_exists():
    populate_data()
    des_exists = ContentDescription.exists()
    assert isinstance(des_exists, int)


def test_update_one():
    populate_data()
    description = "Description one"
    ContentDescription.update_one(
        {"description": description}, {"$set": {"order": -100}}
    )
    assert ContentDescription.get({"description": description}).order == -100


def test_update_many():
    populate_data()
    description = "Description one"
    ContentDescription.update_many(
        {"description": description}, {"$set": {"order": -100}}
    )

    assert ContentDescription.get({"description": description}).order == -100


def test_delete_one():
    populate_data()
    description = "Description one"
    ContentDescription.delete_one({"description": description})

    assert ContentDescription.exists({"description": description}) is False


def test_delete_many():
    populate_data()
    description = "Description one"
    ContentDescription.delete_many({"description": description})

    assert ContentDescription.exists({"description": description}) is False


def test_child_aggregation():
    populate_data()
    for obj in ContentDescription.aggregate(pipeline=[]):
        assert isinstance(obj._id, ObjectId)


def test_child_get_random_one():
    populate_data()
    course = Course.get(filter={})
    ContentDescription(course_id=course._id, description="Demo Description").create()
    obj = ContentDescription.get_random_one()
    assert isinstance(obj._id, ObjectId)
