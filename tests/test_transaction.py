import logging
from time import sleep
from typing import Any
from uuid import uuid4

from mongodb_odm.models import Document
from pymongo.errors import OperationFailure

from .conftest import init_config  # noqa
from .models.course import Course
from .models.user import get_user

logger = logging.getLogger(__name__)


def test_create_with_transaction():
    user = get_user()

    course: Any = None
    with Document.start_session() as session:
        with session.start_transaction():
            course = Course(
                author_id=user._id,
                title="Course Title",
            ).create(session=session)
            session.commit_transaction()  # This will automatically apply if not called explicitly.

    if course:
        # Sleep for 5 seconds to replicate the dataset.
        sleep(5)
        assert (
            Course.find_one({"_id": course.id}) is not None
        ), "Course should be created"


def test_create_with_transaction_rollback():
    user = get_user()

    course: Any = None
    with Document.start_session() as session:
        with session.start_transaction():
            try:
                course = Course(
                    author_id=user._id,
                    title="Course Title",
                ).create(session=session)
                raise Exception("Custom error on transaction")
            except OperationFailure:
                # abort the transaction if an error occurs
                session.abort_transaction()
            except Exception:
                session.abort_transaction()

    if course:
        # Sleep for 5 seconds to replicate the dataset.
        sleep(5)
        assert (
            Course.find_one({"_id": course.id}) is None
        ), "Course should not be created"


def test_update_with_transaction_rollback():
    user = get_user()

    # Use uuid4 to make the title unique for async testing.
    course_title = f"Course Title {uuid4()}"
    course: Course = Course(
        author_id=user._id,
        title=course_title,
    ).create()

    with Document.start_session() as session:
        with session.start_transaction():
            try:
                course.title = "Title Updated"
                course.update(session=session)
                raise Exception("Custom error on transaction")
            except Exception:
                session.abort_transaction()

    # Sleep for 5 seconds to replicate the dataset.
    sleep(5)
    course = Course.get({"_id": course.id})
    assert course.title == course_title, "Course title should not be updated"
