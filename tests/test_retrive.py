import pytest
from bson import ObjectId
from mongodb_odm import DESCENDING
from mongodb_odm.data_conversion import ODMObj

from tests.conftest import INIT_CONFIG
from tests.models.course import Comment, Content, Course
from tests.models.user import User
from tests.utils import create_users, populate_data


@pytest.mark.usefixtures(INIT_CONFIG)
def test_find_one():
    populate_data()
    course = Course.find_one()
    assert isinstance(course, Course), (
        "Each object should carry all characteristic of model"
    )
    assert isinstance(course.id, ObjectId), "Invalid data return"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_count():
    populate_data()
    course_count = Course.count_documents()
    assert isinstance(course_count, int), (
        "count_documents method should return int type value"
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_is_exists():
    populate_data()
    is_exists = Course.exists()
    assert isinstance(is_exists, bool), (
        "count_documents method should return int type value"
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_find():
    populate_data()
    course_qs = Course.find(limit=10)
    for course in course_qs:
        assert isinstance(course, Course), (
            "find method should return Course type object"
        )
        assert isinstance(course.id, ObjectId), "Invalid data return"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_embedded_filter():
    populate_data()
    user = User.get({})
    for _ in Comment.find(filter={"children.user_id": user.id}):
        pass


@pytest.mark.usefixtures(INIT_CONFIG)
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


@pytest.mark.usefixtures(INIT_CONFIG)
def test_aggregate():
    populate_data()
    course_qs = Course.aggregate(pipeline=[])
    for course in course_qs:
        assert isinstance(course, ODMObj), (
            "aggregate method should return dict type object"
        )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_get_random_one():
    populate_data()

    user = User.get({})

    course = Course.get_random_one(filter={"author_id": user.id})
    assert isinstance(course, Course), (
        "get_random_one method should return Course type object"
    )

    assert course.author_id == user.id, "Random course author_id should match"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_find_inheritance_object():
    populate_data()
    for content in Content.find(limit=10):
        assert isinstance(content, Content), (
            "Each object should carry all characteristic of model"
        )
        assert isinstance(content.id, ObjectId), "Invalid data return"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_get_db_name():
    collection_name = Course._db()
    assert isinstance(collection_name, str)

    assert collection_name == "course"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_find_raw():
    populate_data()

    for course in Course.find_raw(limit=2):
        assert isinstance(course, dict), (
            "Each object should carry all characteristic of model"
        )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_id_transformation():
    create_users()

    user = User.find_one({"username": "two"})

    def validate_user(u, new_user):
        assert isinstance(new_user, User)
        assert isinstance(new_user.id, ObjectId)
        assert u.id == new_user.id

    retriveed_data = User.find_one({"id": user.id})
    validate_user(user, retriveed_data)

    retriveed_data = User.find_one({"_id": user.id})
    validate_user(user, retriveed_data)

    total_user = 0
    for _ in User.find({"id": user.id}):
        total_user += 1

    assert total_user == 1


@pytest.mark.usefixtures(INIT_CONFIG)
def test_projection_for_find_raw():
    populate_data()

    for obj in Course.find_raw(projection={"_id": 1}):
        assert isinstance(obj["_id"], ObjectId)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_projection_for_find():
    populate_data()

    for obj in Course.find(projection={"short_description": 0, "cover_image": 0}):
        assert isinstance(obj.id, ObjectId)
        assert obj.cover_image is None
        assert obj.short_description is None


@pytest.mark.usefixtures(INIT_CONFIG)
def test_sort():
    populate_data()

    for obj in Course.find(sort=[("_id", DESCENDING)]):
        assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_skip():
    populate_data()

    for obj in Course.find(skip=2):
        assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_limit():
    populate_data()

    for obj in Course.find(limit=10):
        assert isinstance(obj.id, ObjectId)
