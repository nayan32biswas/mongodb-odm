from time import sleep
from uuid import uuid4

import pytest
from mongodb_odm import ODMObjectId
from mongodb_odm.exceptions import InvalidConfiguration
from mongodb_odm.models import Document
from pymongo.errors import OperationFailure

from tests.conftest import INIT_CONFIG
from tests.models.course import Course


@pytest.mark.usefixtures(INIT_CONFIG)
def test_create_with_transaction():
    author_id = ODMObjectId()

    with Document.start_session() as session:
        with session.start_transaction():
            _ = Course(
                author_id=author_id,
                title="Course Title",
            ).create(session=session)
            session.commit_transaction()  # This will automatically apply if not called explicitly.

    # Sleep for 1 seconds to replicate the dataset.
    sleep(1)
    temp_course = Course.find_one({Course.author_id: author_id})
    assert temp_course is not None, "Course should be created"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_create_with_transaction_rollback():
    author_id = ODMObjectId()

    with Document.start_session() as session:
        with session.start_transaction():
            try:
                _ = Course(
                    author_id=author_id,
                    title="Course Title",
                ).create(session=session)
                raise Exception("Custom error on transaction")
            except OperationFailure:
                # abort the transaction if an error occurs
                session.abort_transaction()
            except Exception:
                session.abort_transaction()

    # Sleep for 1 seconds to replicate the dataset.
    sleep(1)
    temp_course = Course.find_one({Course.author_id: author_id})
    assert temp_course is None, "Course should not be created"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_with_transaction_rollback():
    author_id = ODMObjectId()

    # Use uuid4 to make the title unique for async testing.
    course_title = f"Course Title {uuid4()}"
    course: Course = Course(
        author_id=author_id,
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

    # Sleep for 1 seconds to replicate the dataset.
    sleep(1)
    course = Course.get({Course.id: course.id})
    assert course.title == course_title, "Course title should not be updated"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_try_to_open_transaction_with_async_connection():
    with pytest.raises(InvalidConfiguration) as exc_info:
        with Document.astart_session():
            pass

    assert type(exc_info.value) is InvalidConfiguration, (
        "Should raise InvalidConfiguration when trying to open a transaction with async connection"
    )
