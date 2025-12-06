import pytest
from bson import ObjectId
from mongodb_odm import ODMObjectId

from tests.conftest import ASYNC_INIT_CONFIG
from tests.models.course import Course


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_create_course():
    course = await Course(
        author_id=ODMObjectId(),
        title="New Course Title",
    ).acreate()

    db_course = await Course.afind_one({Course.id: course.id})

    assert db_course is not None, "Course should be created in the database"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_acreate_with_all_fields():
    # Test creating a course with all available fields
    author_id = ODMObjectId()
    course = await Course(
        author_id=author_id,
        title="Complete Course Title",
        short_description="This is a short description of the course",
    ).acreate()

    # Verify the course was created with all fields
    db_course = await Course.afind_one({Course.id: course.id})

    assert db_course is not None, "Course should be created in the database"
    assert db_course.author_id == author_id, "Author ID should match"
    assert db_course.title == "Complete Course Title", "Title should match"
    assert db_course.short_description == "This is a short description of the course", (
        "Description should match"
    )
    assert isinstance(db_course.id, ODMObjectId), "ID should be ODMObjectId type"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_acreate_multiple_courses():
    # Test creating multiple courses asynchronously
    author_id = ODMObjectId()
    courses = []

    for i in range(5):
        course = await Course(
            author_id=author_id,
            title=f"Course {i + 1}",
            short_description=f"Description for course {i + 1}",
        ).acreate()
        courses.append(course)

    # Verify all courses were created
    assert len(courses) == 5, "Should have created 5 courses"

    # Verify each course has unique ID
    course_ids = [course.id for course in courses]
    assert len(set(course_ids)) == 5, "All course IDs should be unique"

    # Verify all courses exist in database
    for course in courses:
        db_course = await Course.afind_one({Course.id: course.id})
        assert db_course is not None, f"Course {course.title} should exist in database"
        assert db_course.author_id == author_id, "Author ID should match"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_acreate_with_kwargs():
    # Test creating a course with additional kwargs passed to MongoDB
    author_id = ODMObjectId()

    # Create course with bypass_document_validation kwarg
    course = await Course(
        author_id=author_id,
        title="Course with Kwargs",
    ).acreate(bypass_document_validation=True)

    # Verify the course was created successfully
    db_course = await Course.afind_one({Course.id: course.id})
    assert db_course is not None, "Course should be created even with kwargs"
    assert db_course.title == "Course with Kwargs", "Title should match"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_acreate_id_generation():
    # Test that IDs are automatically generated when not provided
    author_id = ODMObjectId()

    course = await Course(
        author_id=author_id,
        title="Auto ID Course",
    ).acreate()

    # Verify ID was automatically generated
    assert course.id is not None, "ID should be automatically generated"
    # Check for either ODMObjectId or ObjectId (since ODMObjectId inherits from ObjectId)
    assert isinstance(course.id, ObjectId), "ID should be ODMObjectId or ObjectId type"
    assert course._id == course.id, "_id and id should be the same"

    # Verify the generated ID is valid and exists in database
    db_course = await Course.afind_one({"_id": course.id})
    assert db_course is not None, "Course should exist with generated ID"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_acreate_return_value():
    # Test that acreate returns the same instance with updated ID
    author_id = ODMObjectId()

    original_course = Course(
        author_id=author_id,
        title="Return Value Test",
    )

    # Store original object reference
    original_id = id(original_course)

    created_course = await original_course.acreate()

    # Verify the same instance is returned
    assert id(created_course) == original_id, "Should return the same instance"
    assert created_course is original_course, "Should be the same object reference"
    assert created_course.id is not None, "ID should be set after creation"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_acreate_with_none_values():
    # Test creating a course with None values (should be excluded)
    author_id = ODMObjectId()

    course = await Course(
        author_id=author_id,
        title="Course with None",
        short_description=None,  # This should be excluded from database
    ).acreate()

    # Verify the course was created
    db_course = await Course.afind_one({Course.id: course.id})
    assert db_course is not None, "Course should be created"
    assert db_course.title == "Course with None", "Title should be preserved"

    # Note: short_description might be None in the model but excluded from database
    # This depends on the model's to_mongo() implementation
