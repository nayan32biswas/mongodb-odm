from .models.course import (
    Comment,
    ContentDescription,
    ContentImage,
    Course,
    EmbeddedComment,
)
from .models.user import User


def create_users():
    User(username="one", full_name="Full Name").create()
    User(username="two", full_name="Full Name").create()
    User(username="three", full_name="Full Name").create()


def create_courses():
    user_one = User.get({"username": "one"})
    user_two = User.get({"username": "two"})

    one = Course(
        author_id=user_one.id, title="one", short_description="short description one"
    ).create()
    ContentDescription(course_id=one.id, description="Description one").create()
    ContentImage(course_id=one.id, image_path="/media/one.png").create()

    two = Course(
        author_id=user_two.id, title="two", short_description="short description two"
    ).create()
    ContentDescription(course_id=two.id, description="Description two").create()
    ContentImage(course_id=two.id, image_path="/media/two.png").create()


def create_comments():
    user_one = User.get({"username": "one"})
    user_three = User.get({"username": "three"})

    course_one = Course.get({"title": "one"})
    course_two = Course.get({"title": "two"})

    comment_one = Comment(
        course_id=course_one.id, user_id=user_three.id, description="Comment One"
    ).create()
    Comment(
        course_id=course_two.id, user_id=user_three.id, description="Comment Two"
    ).create()

    comment_one.children.append(
        EmbeddedComment(user_id=user_one.id, description="Child comment one")
    )
    comment_one.update()


def populate_data():
    create_users()
    create_courses()
    create_comments()
