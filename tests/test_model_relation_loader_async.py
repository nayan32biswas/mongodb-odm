from typing import Optional

import pytest
from mongodb_odm import Document, ODMObjectId, Relationship

from tests.conftest import ASYNC_INIT_CONFIG
from tests.models.course import Comment, Course
from tests.models.user import User
from tests.utils import async_create_comments, async_create_courses


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_load_related_data():
    await async_create_courses()

    course_qs = Course.afind()
    courses = await Course.aload_related(course_qs)

    for course in courses:
        assert type(course.author) is User
        assert course.author.id == course.author_id


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_load_related_multiple_data():
    await async_create_comments()

    comment_qs = Comment.afind()
    comments = await Comment.aload_related(comment_qs)

    for comment in comments:
        assert type(comment.user) is User
        assert comment.user.id == comment.user_id

        assert type(comment.course) is Course
        assert comment.course.id == comment.course_id


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_related_data_load_with_field():
    await async_create_comments()

    comment_qs = Comment.afind()
    comments = await Comment.aload_related(comment_qs, fields=["user"])

    for comment in comments:
        assert type(comment.user) is User
        assert comment.user.id == comment.user_id

        assert type(comment.course) is not Course


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_load_related_data_with_invalid_field():
    await async_create_comments()

    try:
        comment_qs = Comment.afind()
        _ = await Comment.aload_related(comment_qs, fields=["invalid"])
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_load_related_data_with_invalid_model():
    class ModelA(Document):
        string: str

    class ModelB(Document):
        a_id: ODMObjectId
        other_field: str

        a: Optional[ModelA] = Relationship(local_field="invalid_id")

    try:
        a = await ModelA(string="a").acreate()
        await ModelB(a_id=a.id, other_field="Other").acreate()
        b_qs = ModelB.afind()
        _ = await ModelB.aload_related(b_qs, fields=["a"])
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_load_related_data_with_optional_object():
    class ModelA(Document):
        string: str

    class ModelB(Document):
        a_id: Optional[ODMObjectId] = None
        other_field: str

        a: Optional[ModelA] = Relationship(local_field="a_id")

    await ModelB(other_field="Other").acreate()

    b_qs = ModelB.afind()
    results = await ModelB.aload_related(b_qs)

    for b in results:
        assert b.a is None
