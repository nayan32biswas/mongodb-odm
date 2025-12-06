import pytest
from mongodb_odm import ODMObjectId

from tests.conftest import ASYNC_INIT_CONFIG
from tests.models.course import Course
from tests.utils import async_create_courses


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aupdate():
    # Create a course to update
    course = await Course(
        author_id=ODMObjectId(),
        title="Original Course Title",
    ).acreate()

    # Test updating with raw dict
    new_title = "Updated Course Title"
    update_result = await course.aupdate(raw={"$set": {"title": new_title}})

    assert update_result.modified_count == 1, "One document should be modified"
    assert update_result.matched_count == 1, "One document should be matched"

    # Verify the update in the database
    db_course = await Course.afind_one({Course.id: course.id})
    assert db_course is not None, "Course should still exist in the database"
    assert db_course.title == new_title, "Course title should be updated"

    # Test updating by modifying object fields
    course.title = "Another Updated Title"
    update_result = await course.aupdate()

    assert update_result.modified_count == 1, "One document should be modified"
    assert update_result.matched_count == 1, "One document should be matched"

    # Verify the update in the database
    db_course = await Course.afind_one({Course.id: course.id})
    assert db_course is not None, "Course should still exist in the database"
    assert db_course.title == "Another Updated Title", (
        "Course title should be updated again"
    )

    # Test updating with kwargs
    update_result = await course.aupdate(upsert=False)

    assert update_result.modified_count == 1, "One document should be modified"
    assert update_result.matched_count == 1, "One document should be matched"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aupdate_one():
    # Create multiple courses to test selective updating
    courses = await async_create_courses(2)
    course1 = courses[0]
    course2 = courses[1]
    author_id = course1.author_id
    initial_title = course2.title

    # Test updating one specific document by ID
    new_title = "Updated Course 1"
    update_result = await Course.aupdate_one(
        {Course.id: course1.id},
        {"$set": {Course.title: new_title}},
    )

    assert update_result.modified_count == 1, "One document should be modified"
    assert update_result.matched_count == 1, "One document should be matched"

    # Verify the correct document was updated
    db_course1 = await Course.afind_one({Course.id: course1.id})
    db_course2 = await Course.afind_one({Course.id: course2.id})

    assert db_course1 is not None, "Course 1 should exist in the database"
    assert db_course1.title == new_title, "Course 1 title should be updated"
    assert db_course2 is not None, "Course 2 should exist in the database"
    assert db_course2.title == initial_title, "Course 2 title should remain unchanged"

    # Test updating with filter that matches multiple documents but only updates one
    update_result = await Course.aupdate_one(
        {Course.author_id: author_id},
        {"$set": {Course.title: "Updated by Author Filter"}},
    )

    assert update_result.modified_count == 1, "Only one document should be modified"
    assert update_result.matched_count == 1, "Only one document should be matched"

    # Test updating with filter that matches no documents
    non_existent_id = ODMObjectId()
    update_result = await Course.aupdate_one(
        {Course.id: non_existent_id},
        {"$set": {Course.title: "This should not update"}},
    )

    assert update_result.modified_count == 0, "No documents should be modified"
    assert update_result.matched_count == 0, "No documents should be matched"

    # Test with upsert=True to create a new document
    new_course_id = ODMObjectId()
    update_result = await Course.aupdate_one(
        {Course.id: new_course_id},
        {"$set": {Course.title: "Upserted Course", Course.author_id: author_id}},
        upsert=True,
    )

    assert update_result.modified_count == 0, "No existing document should be modified"
    assert update_result.matched_count == 0, "No existing document should be matched"
    assert update_result.upserted_id == new_course_id, "New document should be upserted"

    # Verify the upserted document exists
    upserted_course = await Course.afind_one({Course.id: new_course_id})
    assert upserted_course is not None, "Upserted course should exist in the database"
    assert upserted_course.title == "Upserted Course", (
        "Upserted course should have correct title"
    )


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aupdate_many():
    # Create multiple courses with the same author for testing bulk updates
    total_courses = 3
    courses = await async_create_courses(total_courses)
    author_id = courses[0].author_id

    # Create a course with different author_id that should not be updated
    other_author_id = ODMObjectId()
    other_course = await Course(
        author_id=other_author_id,
        title="Other Course",
    ).acreate()

    # Test updating multiple documents by author_id
    update_result = await Course.aupdate_many(
        {Course.author_id: author_id}, {"$set": {Course.title: "Updated Course Title"}}
    )

    assert update_result.modified_count == 3, "Three documents should be modified"
    assert update_result.matched_count == 3, "Three documents should be matched"

    # Verify all courses with the same author_id were updated
    updated_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        updated_courses.append(course)

    assert len(updated_courses) == 3, "Should find 3 updated courses"
    for course in updated_courses:
        assert course.title == "Updated Course Title", (
            "All courses should have updated title"
        )

    # Verify the course with different author_id was not updated
    untouched_course = await Course.afind_one({Course.id: other_course.id})
    assert untouched_course is not None, "Other course should still exist"
    assert untouched_course.title == "Other Course", (
        "Other course title should remain unchanged"
    )

    # Test updating with filter that matches no documents
    update_result = await Course.aupdate_many(
        {Course.author_id: ODMObjectId()},  # Non-existent author
        {"$set": {Course.title: "This should not update"}},
    )

    assert update_result.modified_count == 0, "No documents should be modified"
    assert update_result.matched_count == 0, "No documents should be matched"

    # Test updating all documents (no filter restrictions)
    update_result = await Course.aupdate_many(
        {},  # Empty filter matches all documents
        {"$set": {Course.short_description: "Global update"}},
    )

    assert update_result.modified_count == 4, "All four documents should be modified"
    assert update_result.matched_count == 4, "All four documents should be matched"

    # Verify all documents were updated
    all_courses = []
    async for course in Course.afind({}):
        all_courses.append(course)

    assert len(all_courses) == 4, "Should find all 4 courses"
    for course in all_courses:
        assert hasattr(course, "short_description"), (
            "All courses should have short_description field"
        )

    # Test updating with multiple field changes
    update_result = await Course.aupdate_many(
        {Course.author_id: author_id},
        {
            "$set": {Course.title: "Final Title", "status": "active"},
            "$unset": {Course.short_description: ""},
        },
    )

    assert update_result.modified_count == 3, "Three documents should be modified"
    assert update_result.matched_count == 3, "Three documents should be matched"

    # Verify complex update was applied
    final_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        final_courses.append(course)

    for course in final_courses:
        assert course.title == "Final Title", "Title should be updated to Final Title"
        # Note: status and short_description fields may not be part of the Course model,
        # but the update operation
