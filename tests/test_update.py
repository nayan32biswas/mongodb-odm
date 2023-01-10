import logging

from .models.user import get_user

from .conftest import init_config  # noqa
from .models.post import Post


logger = logging.getLogger(__name__)

UPDATE_TITLE = "Update Title"


def get_new_post():
    user = get_user()
    post = Post(author=user.id, title="Post Title").create()
    return post


def test_update_model():
    post = get_new_post()
    post.title = UPDATE_TITLE
    post.update()

    updated_post = Post.get({"_id": post.id})
    assert updated_post.title == UPDATE_TITLE, "Update Model has no impact on DB."

    post.delete()


def test_update_model_raw():
    post = get_new_post()
    post.update({"$set": {"title": UPDATE_TITLE}})
    updated_post = Post.get({"_id": post.id})
    assert updated_post.title == UPDATE_TITLE, "Update Model has no impact on DB."

    post.update({"$unset": {"title": 1}})
    for obj in Post.find_raw({"_id": post.id}):
        assert obj.get("title") is None

    post.delete()


def test_update_one():
    post = get_new_post()

    updated_post = Post.update_one(
        filter={"_id": post.id}, data={"$set": {"title": UPDATE_TITLE}}
    )
    updated_post = Post.get({"_id": post.id})
    assert updated_post.title == UPDATE_TITLE, "Update One has no impact on DB."

    post.delete()


def test_update_many():
    post1 = get_new_post()
    post2 = get_new_post()

    updated_post = Post.update_many(
        filter={"_id": {"$in": [post1.id, post2.id]}},
        data={"$set": {"title": UPDATE_TITLE}},
    )

    assert updated_post.matched_count == 2, "Total post was not modefied properly."

    total_update = Post.count_documents(
        filter={"_id": {"$in": [post1.id, post2.id]}, "title": UPDATE_TITLE},
    )
    assert total_update == 2, "Update Many has no impact on DB."

    post1.delete()
