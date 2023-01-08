import logging
from datetime import datetime
from bson import ObjectId

from .conftest import init_config  # noqa

from mongodb_odm import DESCENDING
from mongodb_odm.data_conversion import OdmObj
from .models.post import Content, ContentDescription, ContentImage, Post  # noqa
from .models.comment import Comment, EmbeddedComment
from .models.user import get_user


logger = logging.getLogger(__name__)


def populate_data():
    # init_config()
    if Post.exists({"title": "Populate Data"}):
        return
    user = get_user()
    posts = []

    posts.append(Post(author=user.id, title="Populate Data", is_publish=True).create())
    posts.append(
        Post(author=user.id, title="Populate Data One", is_publish=True).create()
    )

    for post in posts:
        for _ in range(3):
            ContentDescription(post=post.id, description="Demo description").create()
        for _ in range(4):
            ContentImage(post=post.id, image_path="/demo/image.png").create()
        for _ in range(4):
            comment = Comment(
                post=post.id,
                user=user.id,
                description="Comment",
            )
            for _ in range(4):
                comment.childs.append(EmbeddedComment(user=user.id, description=""))


def test_find_first():
    populate_data()
    post = Post.find_first()
    assert isinstance(post, Post), "Each object should carry all characteristic of model"
    assert isinstance(post.id, ObjectId), "Invalid data return"


def test_find_last():
    populate_data()
    post = Post.find_last()
    assert isinstance(post, Post), "Each object should carry all characteristic of model"
    assert isinstance(post.id, ObjectId), "Invalid data return"


def test_count():
    post_count = Post.count_documents()
    assert isinstance(
        post_count, int
    ), "count_documents method should return int type value"


def test_is_exists():
    is_exists = Post.exists()
    assert isinstance(
        is_exists, bool
    ), "count_documents method should return int type value"


def test_find():
    post_qs = Post.find(limit=10)
    for post in post_qs:
        assert isinstance(post, Post), "find method should return Post type object"
        assert isinstance(post.id, ObjectId), "Invalid data return"


def test_get_or_create():
    user, title = get_user(), "Title"
    created_at = datetime.utcnow().replace(microsecond=0)

    post, created = Post.get_or_create(
        {"author": user.id, "title": title, "created_at": created_at}
    )
    assert created is True, "New post should be created"
    assert isinstance(post, Post), "Type should be Post"

    post, created = Post.get_or_create(
        {"author": user.id, "title": title, "created_at": created_at}
    )
    assert created is False, "Old post should get from DB"
    assert isinstance(post, Post), "Type should be Post"


def test_aggregate():
    post_qs = Post.aggregate(pipeline=[])
    for post in post_qs:
        assert isinstance(post, OdmObj), "aggregate method should return dict type object"


def test_get_random_one():
    user = get_user()
    post = Post.get_random_one(filter={"author": user.id})
    assert isinstance(post, Post), "get_random_one method should return Post type object"

    assert post.author == user.id, "Random post author should match"


def test_find_inheritance_object():
    for content in Content.find(limit=10):
        assert isinstance(
            content, Content
        ), "Each object should carry all characteristic of model"
        assert isinstance(content.id, ObjectId), "Invalid data return"


def test_get_db_name():
    collection_name = Post._db()
    assert isinstance(collection_name, str)

    assert collection_name == "post"


def test_find_raw():
    for post in Post.find_raw(limit=2):
        assert isinstance(
            post, dict
        ), "Each object should carry all characteristic of model"


def test_projection():
    for obj in Post.find_raw(projection={"_id": 1}):
        assert isinstance(obj["_id"], ObjectId)


def test_sort():
    for obj in Post.find(sort=[("_id", DESCENDING)]):
        assert isinstance(obj.id, ObjectId)


def test_skip():
    for obj in Post.find(skip=2):
        assert isinstance(obj.id, ObjectId)


def test_limit():
    for obj in Post.find(limit=10):
        assert isinstance(obj.id, ObjectId)
