import logging

from .conftest import init_config  # noqa

from .models.post import ContentDescription, ContentImage, Post, Content  # noqa
from .models.user import get_user


logger = logging.getLogger(__name__)


def test_create_post():
    user = get_user()
    _ = Post(
        author=user.id,
        title="Post Title",
        is_publish=True,
    ).create()


def test_inheritance_model_create():
    user = get_user()
    post = Post(
        author=user.id,
        title="Post Title",
        is_publish=True,
        short_description="Short Description",
    ).create()

    content_description = ContentDescription(
        post=post.id, description="Long Description...."
    ).create()

    content_image = ContentImage(
        post=post.id, image_path="/image/path/image.png"
    ).create()

    content_count = Content.count_documents(
        {"_id": {"$in": [content_description.id, content_image.id]}}
    )

    assert (
        content_count == 2
    ), "Content count should be 2 as ContentDescription and ContentImage belong to Content collection"
