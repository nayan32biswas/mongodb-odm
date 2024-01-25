import logging

from .conftest import init_config  # noqa
from .models.course import Content, ContentDescription, ContentImage, Course
from .models.user import get_user

logger = logging.getLogger(__name__)


def test_create_course():
    user = get_user()
    _ = Course(
        author_id=user.id,
        title="Course Title",
    ).create()


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

    assert (
        content_count == 2
    ), "Content count should be 2 as ContentDescription and ContentImage belong to Content collection"
