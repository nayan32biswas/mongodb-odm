from typing import Optional

import pytest
from bson import ObjectId
from mongodb_odm import (
    ASCENDING,
    DESCENDING,
    Document,
    Field,
    ODMObjectId,
    Relationship,
)

from tests.conftest import INIT_CONFIG
from tests.models.course import (
    Content,
    ContentDescription,
    ContentImage,
    Course,
    ImageStyle,
)
from tests.utils import (
    TOTAL_CONTENT,
    TOTAL_DESCRIPTIONS,
    TOTAL_IMAGES,
    populate_data,
)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_find():
    populate_data()

    total_content_count = 0
    for obj in Content.find():
        assert isinstance(obj.id, ObjectId)
        total_content_count += 1

        if isinstance(obj, ContentDescription):
            assert hasattr(obj, "description")
        elif isinstance(obj, ContentImage):
            assert hasattr(obj, "style")
            assert hasattr(obj, "image_path")

    assert total_content_count == TOTAL_CONTENT

    total_image_count = 0
    for obj in ContentImage.find({"style": ImageStyle.LEFT}):
        assert isinstance(obj.id, ObjectId)
        total_image_count += 1

    assert total_image_count == 1

    total_description_count = 0
    for obj in ContentDescription.find():
        assert isinstance(obj.id, ObjectId)
        total_description_count += 1

    assert total_description_count == TOTAL_DESCRIPTIONS


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_find_one():
    populate_data()

    obj = Content.find_one(sort=[("_id", ASCENDING)])
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentDescription)
    assert hasattr(obj, "description")

    obj = ContentImage.find_one({"style": ImageStyle.LEFT})
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentImage)
    assert obj.style == ImageStyle.LEFT

    obj = ContentDescription.find_one()
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentDescription)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_get():
    populate_data()

    obj = Content.get({}, sort=[("_id", DESCENDING)])
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentImage)
    assert hasattr(obj, "image_path")

    obj = ContentImage.get({"style": ImageStyle.LEFT})
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentImage)
    assert obj.style == ImageStyle.LEFT

    obj = ContentDescription.get({})
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentDescription)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_document_count():
    populate_data()

    total_content_count = Content.count_documents()
    assert total_content_count == TOTAL_CONTENT

    description_content_count = ContentDescription.count_documents()
    assert description_content_count == TOTAL_DESCRIPTIONS

    image_content_count = ContentImage.count_documents()
    assert image_content_count == TOTAL_IMAGES


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_exists():
    populate_data()

    content_exists = Content.exists()
    assert content_exists is True

    img_exists = ContentImage.exists({"style": ImageStyle.LEFT})
    assert img_exists is True

    # Delete images with style LEFT
    ContentImage.delete_many({"style": ImageStyle.LEFT})
    img_exists = ContentImage.exists({"style": ImageStyle.LEFT})
    assert img_exists is False

    description_exists = ContentDescription.exists()
    assert description_exists is True

    ContentImage.delete_many({})
    ContentDescription.delete_many({})

    content_exists = Content.exists()
    assert content_exists is False


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_update_one():
    populate_data()

    ContentImage.update_one(
        {"style": ImageStyle.LEFT}, {"$set": {"style": ImageStyle.RIGHT}}
    )

    images = list(Content.find({"style": ImageStyle.RIGHT}))
    assert len(images) == 1
    assert isinstance(images[0], ContentImage)
    assert images[0].style == ImageStyle.RIGHT


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_update_many():
    populate_data()

    ContentImage.update_many({}, {"$set": {"style": ImageStyle.RIGHT}})

    images = list(Content.find({"style": ImageStyle.RIGHT}))
    assert len(images) == TOTAL_IMAGES
    assert isinstance(images[0], ContentImage)
    assert isinstance(images[1], ContentImage)


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_delete_one():
    populate_data()

    ContentImage.delete_one({"style": ImageStyle.RIGHT})
    assert ContentImage.exists({"style": ImageStyle.RIGHT}) is False


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_delete_many():
    populate_data()

    ContentImage.delete_many({"style": ImageStyle.RIGHT})
    assert ContentImage.exists({"style": ImageStyle.RIGHT}) is False


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_child_aggregation():
    populate_data()

    total_image_count = 0
    for obj in ContentImage.aggregate(pipeline=[]):
        assert isinstance(obj.id, ObjectId)
        total_image_count += 1

    assert total_image_count == TOTAL_IMAGES


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_child_get_random_one():
    populate_data()

    course = Course.get(filter={})

    ContentImage(
        course_id=course.id, style=ImageStyle.RIGHT, image_path="path/to/image.jpg"
    ).create()
    obj = ContentImage.get_random_one(
        filter={"course_id": course.id, "style": ImageStyle.RIGHT}
    )

    assert isinstance(obj.id, ObjectId)
    assert obj.style == ImageStyle.RIGHT


@pytest.mark.usefixtures(INIT_CONFIG)
def test_inheritance_model_relation_load_related():
    """
    Test that odm can load data from child model.
    The parent model will not have the related fields of the child model.
    But the child model will have the related fields of the child model.
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

    parent_qs = ParentModel.find(sort=[("_id", ASCENDING)])
    parents = ParentModel.load_related(parent_qs)

    assert len(parents) == 2, "Should have 2 objects"

    parent = parents[0]
    child = parents[1]

    assert isinstance(parent, ParentModel), "First object should be ParentModel"
    assert isinstance(child, ChildModel), "Second object should be ChildModel"

    assert not isinstance(
        child.other, OtherModel
    ), "The related field should not populate the child model fields when loading from parent model"

    # Validate the load data for child model
    child_qs = ChildModel.find(sort=[("_id", ASCENDING)])
    children = ChildModel.load_related(child_qs)

    assert len(children) == 1, "Should have 1 object"

    child = children[0]

    assert isinstance(child, ChildModel), "First object should be ChildModel"

    assert isinstance(child.other, OtherModel), "Related field should be populated"
    assert child.other.title == "demo", "Related field should have correct data"
