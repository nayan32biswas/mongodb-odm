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

    updated_course = Course.get({Course.id: course.id})
    assert updated_course.title == UPDATE_TITLE, "Update Model has no impact on DB."

    course.delete()


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_model_raw():
    populate_data()

    course = Course.get({})
    course.update({"$set": {Course.title: UPDATE_TITLE}})
    updated_course = Course.get({Course.id: course.id})
    assert updated_course.title == UPDATE_TITLE, "Update Model has no impact on DB."

    course.update({"$unset": {Course.title: 1}})
    for obj in Course.find_raw({Course.id: course.id}):
        assert obj.get("title") is None

    course.delete()


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_one():
    populate_data()

    course = Course.get({})

    updated_course = Course.update_one(
        filter={Course.id: course.id}, data={"$set": {Course.title: UPDATE_TITLE}}
    )
    updated_course = Course.get({Course.id: course.id})
    assert updated_course.title == UPDATE_TITLE, "Update One has no impact on DB."

    course.delete()


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_many():
    populate_data()

    course1 = Course.get({Course.title: "one"})
    course2 = Course.get({Course.title: "two"})

    updated_course = Course.update_many(
        filter={Course.id: {"$in": [course1.id, course2.id]}},
        data={"$set": {Course.title: UPDATE_TITLE}},
    )

    assert updated_course.matched_count == 2, "Total course was not modified properly."

    total_update = Course.count_documents(
        filter={
            Course.id: {"$in": [course1.id, course2.id]},
            Course.title: UPDATE_TITLE,
        },
    )
    assert total_update == 2, "Update Many has no impact on DB."

    course1.delete()
