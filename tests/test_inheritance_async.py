import pytest
from bson import ObjectId

from tests.conftest import ASYNC_INIT_CONFIG
from tests.models.course import Content, ContentDescription, Course, ImageStyle
from tests.utils import ASYNC_DESCRIPTION, async_create_contents


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_parent_data_retrieve_async():
    await async_create_contents()

    async for obj in Content.afind():
        assert isinstance(obj.id, ObjectId)

    async for obj in Content.afind({"style": ImageStyle.CENTER}):
        assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_child_data_retrieve_async():
    await async_create_contents()

    async for obj in ContentDescription.afind():
        assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_child_count_async():
    await async_create_contents()

    count = await ContentDescription.acount_documents()
    assert isinstance(count, int)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_child_exists_async():
    await async_create_contents()

    des_exists = await ContentDescription.aexists()
    assert isinstance(des_exists, int)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_update_one_async():
    await async_create_contents()

    await ContentDescription.aupdate_one(
        {"description": ASYNC_DESCRIPTION}, {"$set": {"order": -100}}
    )
    course_description = await ContentDescription.aget(
        {"description": ASYNC_DESCRIPTION}
    )

    assert course_description.order == -100


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_update_many_async():
    await async_create_contents()

    await ContentDescription.aupdate_many(
        {"description": ASYNC_DESCRIPTION}, {"$set": {"order": -100}}
    )
    course_description = await ContentDescription.aget(
        {"description": ASYNC_DESCRIPTION}
    )

    assert course_description.order == -100


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_delete_one_async():
    await async_create_contents()

    description = "Description one"
    await ContentDescription.adelete_one({"description": description})

    assert ContentDescription.exists({"description": description}) is False


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_delete_many_async():
    await async_create_contents()

    description = "Description one"
    await ContentDescription.adelete_many({"description": description})

    assert ContentDescription.exists({"description": description}) is False


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_child_aggregation_async():
    await async_create_contents()

    async for obj in ContentDescription.aaggregate(pipeline=[]):
        assert isinstance(obj.id, ObjectId)


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_child_get_random_one_async():
    await async_create_contents()

    course = await Course.aget(filter={})
    await ContentDescription(
        course_id=course.id, description="Demo Description"
    ).acreate()
    obj = await ContentDescription.aget_random_one()

    assert isinstance(obj.id, ObjectId)


# @pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
# async def test_inheritance_model_relation_load_related_async():
#     """
#     Test that odm can load data from child model even if .
#     """

#     class OtherModel(Document):
#         title: str = Field(...)

#     class ParentModel(Document):
#         title: str = Field(...)

#         class ODMConfig(Document.ODMConfig):
#             allow_inheritance = True

#     class ChildModel(ParentModel):
#         child_title: str = Field(...)
#         other_id: ODMObjectId = Field(...)

#         other: Optional[OtherModel] = Relationship(local_field="other_id")

#         class ODMConfig(Document.ODMConfig): ...

#     other = await OtherModel(title="demo").acreate()

#     await ParentModel(title="demo").acreate()
#     await ChildModel(title="demo", child_title="demo", other_id=other.id).acreate()

#     try:
#         parent_qs = ParentModel.afind()
#         parents = await ParentModel.aload_related(parent_qs)  # should not raise error

#         async for obj in parents:
#             if isinstance(obj, ChildModel):
#                 assert not isinstance(
#                     obj.other, RelationshipInfo
#                 ), "other should have value"

#         raise AssertionError()  # Should raise error before this line
#     except Exception as e:
#         assert str(e) != ""
