import pytest
from mongodb_odm import ODMObjectId

from tests.conftest import ASYNC_INIT_CONFIG
from tests.models.course import Course
from tests.utils import async_create_courses


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_adelete():
    # Create multiple courses to test instance deletion
    total_courses = 3
    courses = await async_create_courses(total_courses)
    author_id = courses[0].author_id

    # Create a course with different author_id that should not be deleted
    other_author_id = ODMObjectId()
    other_course = await Course(
        author_id=other_author_id,
        title="Other Course",
    ).acreate()

    # Test deleting a course instance
    target_course = courses[0]
    original_id = target_course.id

    delete_result = await target_course.adelete()

    assert delete_result.deleted_count == 1, "One document should be deleted"

    # Verify the specific course was deleted
    deleted_course = await Course.afind_one({Course.id: original_id})
    assert deleted_course is None, "Target course should be deleted from the database"

    # Verify other courses with same author still exist
    remaining_same_author_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        remaining_same_author_courses.append(course)

    assert len(remaining_same_author_courses) == 2, (
        "Two courses with same author should remain"
    )

    # Verify the course with different author_id was not affected
    untouched_course = await Course.afind_one({Course.id: other_course.id})
    assert untouched_course is not None, "Other course should still exist"
    assert untouched_course.title == "Other Course", "Other course should be unchanged"

    # Test deleting another course instance
    second_target = courses[1]
    second_original_id = second_target.id

    delete_result = await second_target.adelete()

    assert delete_result.deleted_count == 1, "One document should be deleted"

    # Verify the second course was deleted
    deleted_second_course = await Course.afind_one({Course.id: second_original_id})
    assert deleted_second_course is None, "Second target course should be deleted"

    # Verify only one course with same author remains
    final_same_author_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        final_same_author_courses.append(course)

    assert len(final_same_author_courses) == 1, (
        "One course with same author should remain"
    )

    # Test deleting with kwargs
    third_target = courses[2]
    delete_result = await third_target.adelete(comment="Test deletion with comment")

    assert delete_result.deleted_count == 1, (
        "One document should be deleted with kwargs"
    )

    # Verify all courses with original author are now deleted
    no_same_author_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        no_same_author_courses.append(course)

    assert len(no_same_author_courses) == 0, "No courses with same author should remain"

    # Verify only the other author's course remains
    all_remaining_courses = []
    async for course in Course.afind({}):
        all_remaining_courses.append(course)

    assert len(all_remaining_courses) == 1, "Only one course should remain in total"
    assert all_remaining_courses[0].author_id == other_author_id, (
        "Remaining course should belong to other author"
    )

    # Test attempting to delete an already deleted course (should still work)
    # Create a new course for this test
    new_course = await Course(
        author_id=ODMObjectId(),
        title="Course to Delete Twice",
    ).acreate()

    # First deletion
    first_delete_result = await new_course.adelete()
    assert first_delete_result.deleted_count == 1, "First deletion should succeed"

    # Second deletion (attempting to delete non-existent document)
    second_delete_result = await new_course.adelete()
    assert second_delete_result.deleted_count == 0, (
        "Second deletion should return 0 deleted count"
    )

    # Test deleting course with complex data
    complex_course = await Course(
        author_id=ODMObjectId(),
        title="Complex Course with Special Characters: !@#$%^&*()",
        short_description="This course has a very long description that tests whether deletion works with larger text fields and special characters.",
    ).acreate()

    delete_result = await complex_course.adelete()
    assert delete_result.deleted_count == 1, (
        "Complex course should be deleted successfully"
    )

    # Verify complex course was deleted
    deleted_complex = await Course.afind_one({Course.id: complex_course.id})
    assert deleted_complex is None, "Complex course should be deleted from database"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_adelete_one():
    # Create multiple courses to test selective deletion
    total_courses = 3
    courses = await async_create_courses(total_courses)
    author_id = courses[0].author_id

    # Create a course with different author_id that should not be deleted
    other_author_id = ODMObjectId()
    other_course = await Course(
        author_id=other_author_id,
        title="Other Course",
    ).acreate()

    # Test deleting one specific document by ID
    target_course = courses[0]
    delete_result = await Course.adelete_one({Course.id: target_course.id})

    assert delete_result.deleted_count == 1, "One document should be deleted"

    # Verify the correct document was deleted
    deleted_course = await Course.afind_one({Course.id: target_course.id})
    assert deleted_course is None, "Target course should be deleted from the database"

    # Verify other courses with same author still exist
    remaining_same_author_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        remaining_same_author_courses.append(course)

    assert len(remaining_same_author_courses) == 2, (
        "Two courses with same author should remain"
    )

    # Verify the course with different author_id was not affected
    untouched_course = await Course.afind_one({Course.id: other_course.id})
    assert untouched_course is not None, "Other course should still exist"
    assert untouched_course.title == "Other Course", "Other course should be unchanged"

    # Test deleting with filter that matches multiple documents but only deletes one
    delete_result = await Course.adelete_one({Course.author_id: author_id})

    assert delete_result.deleted_count == 1, "Only one document should be deleted"

    # Verify only one more document was deleted
    final_same_author_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        final_same_author_courses.append(course)

    assert len(final_same_author_courses) == 1, (
        "Only one course with same author should remain"
    )

    # Test deleting with filter that matches no documents
    non_existent_id = ODMObjectId()
    delete_result = await Course.adelete_one({Course.id: non_existent_id})

    assert delete_result.deleted_count == 0, "No documents should be deleted"

    # Verify total remaining documents
    all_remaining_courses = []
    async for course in Course.afind({}):
        all_remaining_courses.append(course)

    assert len(all_remaining_courses) == 2, (
        "Should have 2 total courses remaining (1 same author + 1 other author)"
    )

    # Test deleting with complex filter
    delete_result = await Course.adelete_one(
        {Course.author_id: author_id, Course.title: {"$regex": "Course"}}
    )

    assert delete_result.deleted_count == 1, (
        "One document should be deleted with complex filter"
    )

    # Verify the last course with the target author is deleted
    final_author_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        final_author_courses.append(course)

    assert len(final_author_courses) == 0, (
        "No courses should remain for the original author"
    )

    # Verify only the other author's course remains
    all_final_courses = []
    async for course in Course.afind({}):
        all_final_courses.append(course)

    assert len(all_final_courses) == 1, "Only one course should remain in total"
    assert all_final_courses[0].author_id == other_author_id, (
        "Remaining course should belong to other author"
    )


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_adelete_many():
    # Create multiple courses with the same author for testing bulk deletion
    total_courses = 4
    courses = await async_create_courses(total_courses)
    author_id = courses[0].author_id

    # Create courses with different author_id that should not be deleted
    other_author_id = ODMObjectId()
    other_courses = []
    for i in range(2):
        other_course = await Course(
            author_id=other_author_id,
            title=f"Other Course {i + 1}",
        ).acreate()
        other_courses.append(other_course)

    # Verify initial state
    total_initial_count = await Course.acount_documents({})
    assert total_initial_count == 6, "Should have 6 total courses initially"

    # Test deleting multiple documents by author_id
    delete_result = await Course.adelete_many({Course.author_id: author_id})

    assert delete_result.deleted_count == 4, "Four documents should be deleted"

    # Verify all courses with the same author_id were deleted
    remaining_same_author_courses = []
    async for course in Course.afind({Course.author_id: author_id}):
        remaining_same_author_courses.append(course)

    assert len(remaining_same_author_courses) == 0, (
        "No courses with same author should remain"
    )

    # Verify courses with different author_id were not affected
    remaining_other_courses = []
    async for course in Course.afind({Course.author_id: other_author_id}):
        remaining_other_courses.append(course)

    assert len(remaining_other_courses) == 2, "Both other author courses should remain"
    for course in remaining_other_courses:
        assert course.author_id == other_author_id, (
            "Remaining courses should belong to other author"
        )

    # Test deleting with filter that matches no documents
    non_existent_author = ODMObjectId()
    delete_result = await Course.adelete_many({Course.author_id: non_existent_author})

    assert delete_result.deleted_count == 0, "No documents should be deleted"

    # Verify total count is unchanged
    current_count = await Course.acount_documents({})
    assert current_count == 2, "Should still have 2 courses remaining"

    # Test deleting all remaining documents (empty filter)
    delete_result = await Course.adelete_many({})

    assert delete_result.deleted_count == 2, "All remaining documents should be deleted"

    # Verify all documents are deleted
    final_count = await Course.acount_documents({})
    assert final_count == 0, "No courses should remain after deleting all"

    # Create new test data for complex filter testing
    new_author_id = ODMObjectId()
    for i in range(3):
        await Course(
            author_id=new_author_id,
            title=f"Test Course {i + 1}",
        ).acreate()

    # Create one course with different title pattern
    await Course(
        author_id=new_author_id,
        title="Different Title",
    ).acreate()

    # Test deleting with complex filter (regex pattern)
    delete_result = await Course.adelete_many(
        {Course.author_id: new_author_id, Course.title: {"$regex": "Test Course"}}
    )

    assert delete_result.deleted_count == 3, (
        "Three documents matching regex should be deleted"
    )

    # Verify only the course with different title remains
    remaining_courses = []
    async for course in Course.afind({Course.author_id: new_author_id}):
        remaining_courses.append(course)

    assert len(remaining_courses) == 1, "Only one course should remain"
    assert remaining_courses[0].title == "Different Title", (
        "Remaining course should have different title"
    )

    # Test deleting with multiple field conditions
    another_author_id = ODMObjectId()
    for i in range(2):
        await Course(
            author_id=another_author_id,
            title=f"Multi Field Course {i + 1}",
        ).acreate()

    # Add one more course with same author but different title pattern
    await Course(
        author_id=another_author_id,
        title="No Match Course",
    ).acreate()

    delete_result = await Course.adelete_many(
        {Course.author_id: another_author_id, Course.title: {"$regex": "Multi Field"}}
    )

    assert delete_result.deleted_count == 2, (
        "Two documents with matching conditions should be deleted"
    )

    # Verify final state
    final_all_courses = []
    async for course in Course.afind({}):
        final_all_courses.append(course)

    assert len(final_all_courses) == 2, "Should have 2 courses remaining in total"
