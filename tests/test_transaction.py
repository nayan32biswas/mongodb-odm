import logging
import os
from typing import Any
from uuid import uuid4

from mongodb_odm import connect, disconnect
from mongodb_odm.models import Document
from pymongo.errors import OperationFailure

from .models.course import Course
from .models.user import get_user

logger = logging.getLogger(__name__)


def test_create_with_transaction():
    disconnect()  # disconnect existing connection
    connect(os.environ.get("REMOTE_MONGO_URL", ""))
    user = get_user()
    Course.delete_many()

    course: Any = None
    with Document.start_session() as session:
        with session.start_transaction():
            course = Course(
                author_id=user._id,
                title="Course Title",
            ).create(session=session)
            session.commit_transaction()  # This will automatically apply if not called explicitly.

    if course:
        assert (
            Course.find_one({"_id": course.id}) is not None
        ), "Course should be created"


def test_create_with_transaction_rollback():
    disconnect()  # disconnect existing connection
    connect(os.environ.get("REMOTE_MONGO_URL", ""))
    user = get_user()
    Course.delete_many()

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
        assert (
            Course.find_one({"_id": course.id}) is None
        ), "Course should not be created"


def test_update_with_transaction_rollback():
    disconnect()  # disconnect existing connection
    connect(os.environ.get("REMOTE_MONGO_URL", ""))
    user = get_user()
    Course.delete_many()

    # use uuid4 to make title unique across async testing
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

    if course:
        assert (
            Course.find_one({"title": course_title}) is not None
        ), "Course title should not be updated"
