import pytest
from mongodb_odm import ODMObj, ODMObjectId
from mongodb_odm.exceptions import ObjectDoesNotExist

from tests.conftest import ASYNC_INIT_CONFIG
from tests.models.course import Course
from tests.utils import async_create_courses


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_afind_one():
    course = (await async_create_courses())[0]

    db_course = await Course.afind_one({Course.id: course.id})

    assert db_course is not None, "The course should be found in the database"
    assert db_course.id == course.id, "Course ID should match the created course ID"

    db_course = await Course.afind_one({Course.id: course.id}, sort=[("title", 1)])

    assert db_course is not None, "The course should be found in the database"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_afind_raw():
    course = (await async_create_courses())[0]

    db_course = None
    query = Course.afind_raw({Course.id: course.id})

    async for doc in query:
        db_course = doc

    assert db_course is not None, "Course should be found in the database"
    assert isinstance(db_course, dict), "Course should be a dictionary"
    assert db_course["_id"] == course.id, "Course ID should match the created course ID"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_afind():
    course = (await async_create_courses())[0]

    db_course = None
    query = Course.afind({Course.id: course.id})

    async for doc in query:
        db_course = doc

    assert db_course is not None, "Course should be found in the database"
    assert isinstance(db_course, Course), "Course should be a Course instance"
    assert db_course.id == course.id, "Course ID should match the created course ID"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aget():
    course = (await async_create_courses())[0]

    db_course = await Course.aget({Course.id: course.id})

    assert db_course is not None, "Course should be found in the database"
    assert isinstance(db_course, Course), "Course should be a Course instance"
    assert db_course.id == course.id, "Course ID should match the created course ID"

    with pytest.raises(ObjectDoesNotExist):
        await Course.aget({Course.id: ODMObjectId()})


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aget_or_create():
    new_course_title = "New Course Title"

    # Ensure no existing course with this title
    await Course.adelete_many({Course.title: new_course_title})

    course_author_id = ODMObjectId()
    course, created = await Course.aget_or_create(
        {Course.author_id: course_author_id, Course.title: new_course_title},
    )

    assert created is True, "Course should be created"
    assert isinstance(course, Course), "Course should be a Course instance"

    db_course = await Course.aget({Course.author_id: course.author_id})

    assert db_course is not None, "Course should be found in the database"
    assert isinstance(db_course, Course), "Course should be a Course instance"
    assert db_course.id == course.id, "Course ID should match the created course ID"

    course, created = await Course.aget_or_create(
        {Course.author_id: course_author_id, Course.title: new_course_title},
    )

    assert created is False, "Course should not be created again"
    assert isinstance(course, Course), "Course should be a Course instance"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_acount_documents():
    course = (await async_create_courses())[0]

    count = await Course.acount_documents({Course.author_id: course.author_id})

    assert count == 1, "There should be one course in the database"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aexists():
    course = (await async_create_courses())[0]

    exists = await Course.aexists({Course.author_id: course.author_id})

    assert exists is True, "Course should exist in the database"

    await course.adelete()

    exists = await Course.aexists({"author_id": course.author_id})
    assert exists is False, "Course should not exist in the database after deletion"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aaggregate():
    # Create multiple courses with the same author_id for aggregation
    total_courses = 3
    courses = await async_create_courses(total_courses)
    author_id = courses[0].author_id

    # Create a course with different author_id
    other_author_id = ODMObjectId()
    _ = await async_create_courses(1, author_id=other_author_id)

    pipeline = [{"$match": {Course.author_id: author_id}}]

    results = []
    async for doc in Course.aaggregate(pipeline):
        results.append(doc)

    # Verify the aggregation result
    assert results != [], "Aggregation should return a result"
    assert len(results) == total_courses, (
        f"There should be {total_courses} courses for this author"
    )
    for result in results:
        assert isinstance(result, ODMObj), (
            "Aggregation result should be a ODMObj instance"
        )
        assert result.author_id == author_id, (
            "Author ID should match in aggregation result"
        )

    results = []
    async for doc in Course.aaggregate(pipeline, get_raw=True):
        results.append(doc)

    # Verify the raw result
    assert results != [], "Aggregation should return a result"
    assert len(results) == total_courses, (
        f"There should be {total_courses} courses for this author"
    )
    for result in results:
        assert isinstance(result, dict), "Aggregation result should be a dict instance"
        assert result["author_id"] == author_id, (
            "Author ID should match in aggregation result"
        )


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aget_random_one():
    total_courses = 3
    courses = await async_create_courses(total_courses)
    course_ids = [course.id for course in courses]
    author_id = courses[0].author_id

    # Test getting a random course without filter
    random_course = await Course.aget_random_one()

    assert isinstance(random_course, Course), (
        "Random course should be a Course instance"
    )
    assert random_course.id in course_ids, (
        "Random course ID should be one of the created courses"
    )

    # Test getting a random course with filter
    random_course_filtered = await Course.aget_random_one({"author_id": author_id})

    assert isinstance(random_course_filtered, Course), (
        "Filtered random course should be a Course instance"
    )
    assert random_course_filtered.author_id == author_id, (
        "Random course should match the filter"
    )
    assert random_course_filtered.id in course_ids, (
        "Random course ID should be one of the created courses"
    )

    # Test multiple calls to ensure randomness (they might return different results)
    random_courses = []
    for _ in range(3):
        random_course = await Course.aget_random_one({"author_id": author_id})
        random_courses.append(random_course.id)

    # All returned courses should be valid
    for course_id in random_courses:
        assert course_id in course_ids, "All random course IDs should be valid"

    # Test with filter that matches no documents - should raise ObjectDoesNotExist
    with pytest.raises(ObjectDoesNotExist):
        await Course.aget_random_one({Course.author_id: ODMObjectId()})
