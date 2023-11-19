import logging
from typing import Optional

from mongodb_odm import Document, ODMObjectId, Relationship

from .conftest import init_config  # noqa
from .models.course import Comment, Course
from .models.user import User
from .utils import populate_data

logger = logging.getLogger(__name__)


def test_load_related_data():
    populate_data()

    course_qs = Course.find()
    courses = Course.load_related(course_qs)
    for course in courses:
        assert type(course.author) is User
        assert course.author.id == course.author_id


def test_load_related_multiple_data():
    populate_data()

    comment_qs = Comment.find()
    comments = Comment.load_related(comment_qs)
    for comment in comments:
        assert type(comment.user) is User
        assert comment.user.id == comment.user_id

        assert type(comment.course) is Course
        assert comment.course.id == comment.course_id


def test_related_data_load_with_field():
    populate_data()

    comment_qs = Comment.find()
    comments = Comment.load_related(comment_qs, fields=["user"])
    for comment in comments:
        assert type(comment.user) is User
        assert comment.user.id == comment.user_id

        assert type(comment.course) is not Course


def test_load_related_data_with_invalid_field():
    populate_data()

    try:
        comment_qs = Comment.find()
        _ = Comment.load_related(comment_qs, fields=["invalid"])
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_load_related_data_with_invalid_model():
    class ModelA(Document):
        string: str

    class ModelB(Document):
        a_id: ODMObjectId
        other_field: str

        a: Optional[ModelA] = Relationship(local_field="invalid_id")

    try:
        a = ModelA(string="a").create()
        ModelB(a_id=a.id, other_field="Other").create()
        b_qs = ModelB.find()
        _ = ModelB.load_related(b_qs, fields=["a"])
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


def test_load_related_data_with_optional_object():
    class ModelA(Document):
        string: str

    class ModelB(Document):
        a_id: Optional[ODMObjectId] = None
        other_field: str

        a: Optional[ModelA] = Relationship(local_field="a_id")

    ModelB(other_field="Other").create()

    b_qs = ModelB.find()
    for b in ModelB.load_related(b_qs):
        assert b.a is None
