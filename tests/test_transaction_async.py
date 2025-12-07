from time import sleep
from uuid import uuid4

import pytest
from mongodb_odm import ODMObjectId
from mongodb_odm.exceptions import InvalidConfiguration
from mongodb_odm.models import Document
from pymongo.errors import OperationFailure

from tests.conftest import ASYNC_INIT_CONFIG
from tests.models.course import Course


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_create_with_async_transaction():
    author_id = ODMObjectId()

    async with Document.astart_session() as session:
        async with await session.start_transaction():
            _ = await Course(
                author_id=author_id,
                title="Course Title",
            ).acreate(session=session)
            # This will automatically apply if not called explicitly.
            await session.commit_transaction()

    # Sleep for 1 seconds to replicate the dataset.
    sleep(1)
    temp_course = await Course.afind_one({Course.author_id: author_id})
    assert temp_course is not None, "Course should be created"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_create_with_transaction_rollback_async():
    author_id = ODMObjectId()

    async with Document.astart_session() as session:
        async with await session.start_transaction():
            try:
                _ = await Course(
                    author_id=author_id,
                    title="Course Title",
                ).acreate(session=session)
                raise Exception("Custom error on transaction")
            except OperationFailure:
                # abort the transaction if an error occurs
                await session.abort_transaction()
            except Exception:
                await session.abort_transaction()

    # Sleep for 1 seconds to replicate the dataset.
    sleep(1)
    temp_course = await Course.afind_one({Course.author_id: author_id})
    assert temp_course is None, "Course should not be created"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_update_with_transaction_rollback():
    author_id = ODMObjectId()

    # Use uuid4 to make the title unique for async testing.
    course_title = f"Course Title {uuid4()}"
    course: Course = await Course(
        author_id=author_id,
        title=course_title,
    ).acreate()

    async with Document.astart_session() as session:
        async with await session.start_transaction():
            try:
                course.title = "Title Updated"
                await course.aupdate(session=session)
                raise Exception("Custom error on transaction")
            except Exception:
                await session.abort_transaction()

    # Sleep for 1 seconds to replicate the dataset.
    sleep(1)
    temp_course = await Course.afind_one({Course.author_id: author_id})
    assert temp_course.title == course_title, "Course title should not be updated"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_try_to_open_transaction_with_sync_connection():
    with pytest.raises(InvalidConfiguration) as exc_info:
        with Document.start_session():
            pass

    assert type(exc_info.value) is InvalidConfiguration, (
        "Should raise InvalidConfiguration when trying to open a transaction with async connection"
    )
