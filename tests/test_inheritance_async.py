from typing import Optional

import pytest
from bson import ObjectId
from mongodb_odm import ASCENDING, Document, Field, ODMObjectId, Relationship

from tests.conftest import ASYNC_INIT_CONFIG
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
    async_populate_data,
)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_find_async():
    await async_populate_data()

    total_content_count = 0
    async for obj in Content.afind():
        assert isinstance(obj.id, ObjectId)
        total_content_count += 1

    assert total_content_count == TOTAL_CONTENT

    total_image_count = 0
    async for obj in ContentImage.afind({"style": ImageStyle.LEFT}):
        assert isinstance(obj.id, ObjectId)
        total_image_count += 1

    assert total_image_count == 1

    total_description_count = 0
    async for obj in ContentDescription.afind():
        assert isinstance(obj.id, ObjectId)
        total_description_count += 1

    assert total_description_count == TOTAL_DESCRIPTIONS


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_find_one_async():
    await async_populate_data()

    obj = await Content.afind_one()
    assert isinstance(obj.id, ObjectId)

    obj = await ContentImage.afind_one({"style": ImageStyle.LEFT})
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentImage)
    assert obj.style == ImageStyle.LEFT

    obj = await ContentDescription.afind_one()
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentDescription)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_get_async():
    await async_populate_data()

    obj = await Content.aget({})  # type: ignore
    assert isinstance(obj.id, ObjectId)

    obj = await ContentImage.aget({"style": ImageStyle.LEFT})
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentImage)
    assert obj.style == ImageStyle.LEFT

    obj = await ContentDescription.aget({})
    assert isinstance(obj.id, ObjectId)
    assert isinstance(obj, ContentDescription)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_document_count_async():
    await async_populate_data()

    total_content_count = await Content.acount_documents()
    assert total_content_count == TOTAL_CONTENT

    description_content_count = await ContentDescription.acount_documents()
    assert description_content_count == TOTAL_DESCRIPTIONS

    image_content_count = await ContentImage.acount_documents()
    assert image_content_count == TOTAL_IMAGES


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_exists_async():
    await async_populate_data()

    content_exists = await Content.aexists()
    assert content_exists is True

    img_exists = await ContentImage.aexists({"style": ImageStyle.LEFT})
    assert img_exists is True

    # Delete images with style LEFT
    await ContentImage.adelete_many({"style": ImageStyle.LEFT})
    img_exists = await ContentImage.aexists({"style": ImageStyle.LEFT})
    assert img_exists is False

    description_exists = await ContentDescription.aexists()
    assert description_exists is True

    await ContentImage.adelete_many({})
    await ContentDescription.adelete_many({})

    content_exists = await Content.aexists()
    assert content_exists is False


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_update_one_async():
    await async_populate_data()

    await ContentImage.aupdate_one(
        {"style": ImageStyle.LEFT}, {"$set": {"style": ImageStyle.RIGHT}}
    )

    images = [obj async for obj in Content.afind({"style": ImageStyle.RIGHT})]
    assert len(images) == 1
    assert isinstance(images[0], ContentImage)
    assert images[0].style == ImageStyle.RIGHT


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_update_many_async():
    await async_populate_data()

    await ContentImage.aupdate_many({}, {"$set": {"style": ImageStyle.RIGHT}})

    images = [obj async for obj in Content.afind({"style": ImageStyle.RIGHT})]
    assert len(images) == TOTAL_IMAGES
    assert isinstance(images[0], ContentImage)
    assert isinstance(images[1], ContentImage)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_delete_one_async():
    await async_populate_data()

    await ContentImage.adelete_one({"style": ImageStyle.RIGHT})
    assert await ContentImage.aexists({"style": ImageStyle.RIGHT}) is False


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_delete_many_async():
    await async_populate_data()

    await ContentImage.adelete_many({"style": ImageStyle.RIGHT})
    assert await ContentImage.aexists({"style": ImageStyle.RIGHT}) is False


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_child_aggregation_async():
    await async_populate_data()

    total_image_count = 0
    async for obj in ContentImage.aaggregate(pipeline=[]):
        assert isinstance(obj.id, ObjectId)
        total_image_count += 1

    assert total_image_count == TOTAL_IMAGES


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_child_get_random_one_async():
    await async_populate_data()

    course = await Course.aget(filter={})

    await ContentImage(
        course_id=course.id, style=ImageStyle.RIGHT, image_path="path/to/image.jpg"
    ).acreate()
    obj = await ContentImage.aget_random_one(
        filter={"course_id": course.id, "style": ImageStyle.RIGHT}
    )

    assert isinstance(obj.id, ObjectId)
    assert obj.style == ImageStyle.RIGHT


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_inheritance_model_relation_load_related_async():
    """
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

    other = await OtherModel(title="demo").acreate()

    await ParentModel(title="demo").acreate()
    await ChildModel(title="demo", child_title="demo", other_id=other.id).acreate()

    parent_qs = ParentModel.afind(sort=[("_id", ASCENDING)])
    parents = await ParentModel.aload_related(parent_qs)

    assert len(parents) == 2, "Should have 2 objects"

    parent = parents[0]
    child = parents[1]

    assert isinstance(parent, ParentModel), "First object should be ParentModel"
    assert isinstance(child, ChildModel), "Second object should be ChildModel"

    assert not isinstance(child.other, OtherModel), (
        "The related field should not populate the child model fields when loading from parent model"
    )

    # Validate the load data for child model
    child_qs = ChildModel.afind(sort=[("_id", ASCENDING)])
    children = await ChildModel.aload_related(child_qs)

    assert len(children) == 1, "Should have 1 object"

    child = children[0]

    assert isinstance(child, ChildModel), "First object should be ChildModel"

    assert isinstance(child.other, OtherModel), "Related field should be populated"
    assert child.other.title == "demo", "Related field should have correct data"
