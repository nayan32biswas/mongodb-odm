import pytest

from tests.conftest import INIT_CONFIG
from tests.models.course import Course
from tests.utils import populate_data

UPDATE_TITLE = "Update Title"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_model():
    populate_data()

    course = Course.get({})
    course.title = UPDATE_TITLE
    course.update()

    updated_course = Course.get({"_id": course.id})
    assert updated_course.title == UPDATE_TITLE, "Update Model has no impact on DB."

    course.delete()


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_model_raw():
    populate_data()

    course = Course.get({})
    course.update({"$set": {"title": UPDATE_TITLE}})
    updated_course = Course.get({"_id": course.id})
    assert updated_course.title == UPDATE_TITLE, "Update Model has no impact on DB."

    course.update({"$unset": {"title": 1}})
    for obj in Course.find_raw({"_id": course.id}):
        assert obj.get("title") is None

    course.delete()


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_one():
    populate_data()

    course = Course.get({})

    updated_course = Course.update_one(
        filter={"_id": course.id}, data={"$set": {"title": UPDATE_TITLE}}
    )
    updated_course = Course.get({"_id": course.id})
    assert updated_course.title == UPDATE_TITLE, "Update One has no impact on DB."

    course.delete()


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_many():
    populate_data()

    course1 = Course.get({"title": "one"})
    course2 = Course.get({"title": "two"})

    updated_course = Course.update_many(
        filter={"_id": {"$in": [course1.id, course2.id]}},
        data={"$set": {"title": UPDATE_TITLE}},
    )

    assert updated_course.matched_count == 2, "Total course was not modified properly."

    total_update = Course.count_documents(
        filter={
            "_id": {"$in": [course1.id, course2.id]},
            "title": UPDATE_TITLE,
        },
    )
    assert total_update == 2, "Update Many has no impact on DB."

    course1.delete()
