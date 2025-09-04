from mongodb_odm import ODMObjectId

from tests.models.course import (
    Comment,
    ContentDescription,
    ContentImage,
    Course,
    EmbeddedComment,
)
from tests.models.user import User

ASYNC_DESCRIPTION = "Async Description"


def create_users():
    User(username="one", full_name="Full Name").create()
    User(username="two", full_name="Full Name").create()
    User(username="three", full_name="Full Name").create()


def create_courses():
    user_one = User.get({"username": "one"})
    user_two = User.get({"username": "two"})

    one = Course(
        author_id=user_one.id,
        title="one",
        short_description="short description one",
    ).create()
    ContentDescription(course_id=one.id, description="Description one").create()
    ContentImage(course_id=one.id, image_path="/media/one.png").create()

    two = Course(
        author_id=user_two.id,
        title="two",
        short_description="short description two",
    ).create()
    ContentDescription(course_id=two.id, description="Description two").create()
    ContentImage(course_id=two.id, image_path="/media/two.png").create()


def create_comments():
    user_one = User.get({"username": "one"})
    user_three = User.get({"username": "three"})

    course_one = Course.get({"title": "one"})
    course_two = Course.get({"title": "two"})

    comment_one = Comment(
        course_id=course_one.id,
        user_id=user_three.id,
        description="Comment One",
    ).create()
    Comment(
        course_id=course_two.id,
        user_id=user_three.id,
        description="Comment Two",
    ).create()

    comment_one.children.append(
        EmbeddedComment(user_id=user_one.id, description="Child comment one")
    )
    comment_one.update()


async def async_create_courses(total_courses=1, author_id=None):
    if author_id is None:
        user_one, _ = await User.aget_or_create(
            {"username": "one", "full_name": "Full Name"}
        )
        author_id = user_one.id

    courses = []

    for i in range(total_courses):
        course = await Course(
            author_id=author_id,
            title=f"Random Course {i}",
        ).acreate()

        courses.append(course)

    return courses


async def async_create_contents():
    author_id = ODMObjectId()

    course = await Course(
        author_id=author_id,
        title="Random Course",
    ).acreate()

    content_description = await ContentDescription(
        course_id=course.id, description=ASYNC_DESCRIPTION
    ).acreate()

    content_image = await ContentImage(
        course_id=course.id, image_path="/media/async_image.png"
    ).acreate()

    return content_description, content_image


async def async_create_comments():
    user_one, _ = await User.aget_or_create(
        {"username": "one", "full_name": "Full Name"}
    )
    user_two, _ = await User.aget_or_create(
        {"username": "two", "full_name": "Full Name"}
    )

    course_one = await Course(title="one", author_id=user_one.id).acreate()
    course_two = await Course(title="two", author_id=user_two.id).acreate()

    comment_one = await Comment(
        course_id=course_one.id,
        user_id=user_one.id,
        description="Comment One",
    ).acreate()
    await Comment(
        course_id=course_two.id,
        user_id=user_two.id,
        description="Comment Two",
    ).acreate()

    comment_one.children.append(
        EmbeddedComment(user_id=user_one.id, description="Child comment one")
    )
    await comment_one.update()


def drop_all_user_databases(client):
    databases = client.list_database_names()

    system_dbs = {"admin", "local", "config"}

    for db_name in databases:
        if db_name not in system_dbs:
            client.drop_database(db_name)


async def async_drop_all_user_databases(client):
    databases = await client.list_database_names()

    system_dbs = {"admin", "local", "config"}

    for db_name in databases:
        if db_name not in system_dbs:
            await client.drop_database(db_name)


def populate_data():
    create_users()
    create_courses()
    create_comments()
