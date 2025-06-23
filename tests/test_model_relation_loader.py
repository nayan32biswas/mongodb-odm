from typing import Optional

import pytest
from mongodb_odm import Document, ODMObjectId, Relationship

from tests.conftest import INIT_CONFIG
from tests.models.course import Comment, Course
from tests.models.user import User
from tests.utils import populate_data


@pytest.mark.usefixtures(INIT_CONFIG)
def test_load_related_data():
    populate_data()

    course_qs = Course.find()
    courses = Course.load_related(course_qs)
    for course in courses:
        assert type(course.author) is User
        assert course.author.id == course.author_id


@pytest.mark.usefixtures(INIT_CONFIG)
def test_load_related_multiple_data():
    populate_data()

    comment_qs = Comment.find()
    comments = Comment.load_related(comment_qs)
    for comment in comments:
        assert type(comment.user) is User
        assert comment.user.id == comment.user_id

        assert type(comment.course) is Course
        assert comment.course.id == comment.course_id


@pytest.mark.usefixtures(INIT_CONFIG)
def test_related_data_load_with_field():
    populate_data()

    comment_qs = Comment.find()
    comments = Comment.load_related(comment_qs, fields=["user"])
    for comment in comments:
        assert type(comment.user) is User
        assert comment.user.id == comment.user_id

        assert type(comment.course) is not Course


@pytest.mark.usefixtures(INIT_CONFIG)
def test_load_related_data_with_invalid_field():
    populate_data()

    try:
        comment_qs = Comment.find()
        _ = Comment.load_related(comment_qs, fields=["invalid"])
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


@pytest.mark.usefixtures(INIT_CONFIG)
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


@pytest.mark.usefixtures(INIT_CONFIG)
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
