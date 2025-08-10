from datetime import datetime

import pytest
from mongodb_odm import ODMObjectId

from tests.conftest import INIT_CONFIG
from tests.models.course import Content, ContentDescription, ContentImage, Course
from tests.models.user import User, get_user
from tests.utils import populate_data


@pytest.mark.usefixtures(INIT_CONFIG)
def test_create_course():
    user = get_user()
    _ = Course(
        author_id=user.id,
        title="Course Title",
    ).create()


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_model_create():
    user = get_user()
    course = Course(
        author_id=user.id,
        title="Course Title",
        short_description="Short Description",
    ).create()

    content_description = ContentDescription(
        course_id=course._id, description="Long Description...."
    ).create()

    content_image = ContentImage(
        course_id=course.id, image_path="/image/path/image.png"
    ).create()

    content_count = Content.count_documents(
        {"_id": {"$in": [content_description.id, content_image.id]}}
    )

    assert content_count == 2, (
        "Content count should be 2 as ContentDescription and ContentImage belong to Content collection"
    )


@pytest.mark.usefixtures(INIT_CONFIG)
def test_get_or_create():
    populate_data()
    user = User.get({})
    title = "Title"
    created_at = datetime.now().replace(microsecond=0)

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


@pytest.mark.usefixtures(INIT_CONFIG)
def test_object_initiation_with_id():
    course_id = ODMObjectId()
    user_id = ODMObjectId()

    _ = Course(
        id=course_id,
        author_id=user_id,
        title="Course Title",
    ).create()
