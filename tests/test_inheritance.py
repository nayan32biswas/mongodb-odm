from typing import Optional

import pytest
from bson import ObjectId
from mongodb_odm import Document, Field, ODMObjectId, Relationship
from mongodb_odm.fields import RelationshipInfo

from tests.conftest import INIT_CONFIG
from tests.models.course import Content, ContentDescription, Course, ImageStyle
from tests.utils import populate_data


@pytest.mark.usefixtures(INIT_CONFIG)
def test_parent_data_retrieve():
    populate_data()

    for obj in Content.find():
        assert isinstance(obj.id, ObjectId)

    for obj in Content.find({"style": ImageStyle.CENTER}):
        assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_child_data_retrieve():
    populate_data()
    for obj in ContentDescription.find():
        assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_child_count():
    populate_data()
    count = ContentDescription.count_documents()
    assert isinstance(count, int)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_child_exists():
    populate_data()
    des_exists = ContentDescription.exists()
    assert isinstance(des_exists, int)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_one():
    populate_data()
    description = "Description one"
    ContentDescription.update_one(
        {"description": description}, {"$set": {"order": -100}}
    )
    assert ContentDescription.get({"description": description}).order == -100


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_many():
    populate_data()
    description = "Description one"
    ContentDescription.update_many(
        {"description": description}, {"$set": {"order": -100}}
    )

    assert ContentDescription.get({"description": description}).order == -100


@pytest.mark.usefixtures(INIT_CONFIG)
def test_delete_one():
    populate_data()
    description = "Description one"
    ContentDescription.delete_one({"description": description})

    assert ContentDescription.exists({"description": description}) is False


@pytest.mark.usefixtures(INIT_CONFIG)
def test_delete_many():
    populate_data()
    description = "Description one"
    ContentDescription.delete_many({"description": description})

    assert ContentDescription.exists({"description": description}) is False


@pytest.mark.usefixtures(INIT_CONFIG)
def test_child_aggregation():
    populate_data()
    for obj in ContentDescription.aggregate(pipeline=[]):
        assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_child_get_random_one():
    populate_data()
    course = Course.get(filter={})
    ContentDescription(course_id=course.id, description="Demo Description").create()
    obj = ContentDescription.get_random_one()

    assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_model_relation_load_related():
    """
    Test that odm can load data from child model even if .
    """

    class OtherModel(Document):
        title: str = Field(...)

    class ParentModel(Document):
        title: str = Field(...)

        class ODMConfig(Document.ODMConfig):
            allow_inheritance = True

    class ChildModel(ParentModel):
        child_title: str = Field(...)
        other_id: ODMObjectId = Field(...)

        other: Optional[OtherModel] = Relationship(local_field="other_id")

        class ODMConfig(Document.ODMConfig): ...

    other = OtherModel(title="demo").create()

    ParentModel(title="demo").create()
    ChildModel(title="demo", child_title="demo", other_id=other.id).create()

    try:
        parent_qs = ParentModel.find()
        parents = ParentModel.load_related(parent_qs)  # should not raise error

        for obj in parents:
            if isinstance(obj, ChildModel):
                assert not isinstance(obj.other, RelationshipInfo), (
                    "other should have value"
                )
        raise AssertionError()  # Should raise error before this line
    except Exception as e:
        assert str(e) != ""
