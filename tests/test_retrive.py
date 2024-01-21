import logging
from datetime import datetime

from bson import ObjectId
from mongodb_odm import DESCENDING
from mongodb_odm.connection import get_client
from mongodb_odm.data_conversion import ODMObj

from .conftest import init_config  # noqa
from .models.course import Comment, Content, Course
from .models.user import User
from .utils import populate_data

logger = logging.getLogger(__name__)


def test_find_one():
    get_client().get_database().command("dropDatabase")
    populate_data()
    course = Course.find_one()
    assert isinstance(
        course, Course
    ), "Each object should carry all characteristic of model"
    assert isinstance(course.id, ObjectId), "Invalid data return"


def test_count():
    populate_data()
    course_count = Course.count_documents()
    assert isinstance(
        course_count, int
    ), "count_documents method should return int type value"


def test_is_exists():
    populate_data()
    is_exists = Course.exists()
    assert isinstance(
        is_exists, bool
    ), "count_documents method should return int type value"


def test_find():
    populate_data()
    course_qs = Course.find(limit=10)
    for course in course_qs:
        assert isinstance(
            course, Course
        ), "find method should return Course type object"
        assert isinstance(course.id, ObjectId), "Invalid data return"


def test_embedded_filter():
    populate_data()
    user = User.get({})
    for _ in Comment.find(filter={"children.user_id": user.id}):
        pass


def test_filter_invalid_field_validation():
    populate_data()
    user = User.get({})

    """Check that validation function can validate valid nested field"""
    for _ in Comment.find(filter={"children.user_id": user.id}):
        pass

    try:
        """Check that validation function can validate invalid field"""
        for _ in Comment.find(filter={"children.user_id": user.id, "invalid_key": 1}):
            pass

        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""

    try:
        """Check that validation function can validate invalid nested field"""
        for _ in Comment.find(filter={"children.invalid_nested_key": user.id}):
            pass
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_get_or_create():
    populate_data()
    user = User.get({})
    title = "Title"
    created_at = datetime.utcnow().replace(microsecond=0)

    course, created = Course.get_or_create(
        {"author_id": user.id, "title": title, "created_at": created_at}
    )
    assert created is True, "New course should be created"
    assert isinstance(course, Course), "Type should be Course"

    course, created = Course.get_or_create(
        {"author_id": user.id, "title": title, "created_at": created_at}
    )
    assert created is False, "Old course should get from DB"
    assert isinstance(course, Course), "Type should be Course"


def test_aggregate():
    populate_data()
    course_qs = Course.aggregate(pipeline=[])
    for course in course_qs:
        assert isinstance(
            course, ODMObj
        ), "aggregate method should return dict type object"


def test_get_random_one():
    populate_data()

    user = User.get({})

    course = Course.get_random_one(filter={"author_id": user.id})
    assert isinstance(
        course, Course
    ), "get_random_one method should return Course type object"

    assert course.author_id == user.id, "Random course author_id should match"


def test_find_inheritance_object():
    populate_data()
    for content in Content.find(limit=10):
        assert isinstance(
            content, Content
        ), "Each object should carry all characteristic of model"
        assert isinstance(content.id, ObjectId), "Invalid data return"


def test_get_db_name():
    collection_name = Course._db()
    assert isinstance(collection_name, str)

    assert collection_name == "course"


def test_find_raw():
    populate_data()

    for course in Course.find_raw(limit=2):
        assert isinstance(
            course, dict
        ), "Each object should carry all characteristic of model"


def test_projection_for_find_raw():
    populate_data()

    for obj in Course.find_raw(projection={"_id": 1}):
        assert isinstance(obj["_id"], ObjectId)


def test_projection_for_find():
    populate_data()

    for obj in Course.find(projection={"short_description": 0, "cover_image": 0}):
        assert isinstance(obj.id, ObjectId)
        assert obj.cover_image is None
        assert obj.short_description is None


def test_sort():
    populate_data()

    for obj in Course.find(sort=[("_id", DESCENDING)]):
        assert isinstance(obj.id, ObjectId)


def test_skip():
    populate_data()

    for obj in Course.find(skip=2):
        assert isinstance(obj.id, ObjectId)


def test_limit():
    populate_data()

    for obj in Course.find(limit=10):
        assert isinstance(obj.id, ObjectId)
