import logging
from bson import ObjectId


from .conftest import init_config, DB_URL  # noqa
from .models.post import Content, ContentDescription, Post

logger = logging.getLogger(__name__)


def test_parent_data_retrive():
    for obj in Content.find():
        assert isinstance(obj.id, ObjectId)


def test_child_data_retrive():
    for obj in ContentDescription.find():
        assert isinstance(obj.id, ObjectId)


def test_child_count():
    count = ContentDescription.count_documents()
    assert isinstance(count, int)


def test_child_exists():
    des_exists = ContentDescription.exists()
    assert isinstance(des_exists, int)


def test_child_aggregation():
    for obj in ContentDescription.aggregate(pipeline=[]):
        assert isinstance(obj["_id"], ObjectId)


def test_child_get_random_one():
    post = Post.get()
    ContentDescription(post=post.id, description="Demo Description").create()
    obj = ContentDescription.get_random_one()
    assert isinstance(obj.id, ObjectId)
