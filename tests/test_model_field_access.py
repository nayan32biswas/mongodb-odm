import pytest
from mongodb_odm import Document, Field
from pydantic import BaseModel

from tests.conftest import ASYNC_INIT_CONFIG, INIT_CONFIG


class Player(Document):
    name: str = Field()
    age: int


class Game(Document):
    title: str = Field(alias="game_title")


class Address(BaseModel):
    city: str = Field()
    zip_code: int


class User(Document):
    name: str = Field()
    address: Address


def test_field_access():
    assert Player.name == "name"
    assert Player.age == "age"

    try:
        Player.unknown  # noqa
        assert False, "Should raise AttributeError"  # noqa
    except AttributeError:
        pass


def test_field_access_with_alias():
    # Pydantic stores fields by their attribute name, not alias
    assert Game.title == "title"


def test_id_field_access():
    assert Player.id == "_id"


def test_inheritance():
    class ProPlayer(Player):
        team: str

    assert ProPlayer.name == "name"
    assert ProPlayer.team == "team"


def test_db_query():
    # This test requires a database connection, which might not be set up in this isolated file
    # unless we use fixtures. However, we can test the dictionary construction which is what matters.

    query = {Player.name: "Pelé"}
    assert query == {"name": "Pelé"}

    query_alias = {Game.title: "FIFA"}
    assert query_alias == {"title": "FIFA"}


@pytest.mark.usefixtures(INIT_CONFIG)
def test_find_with_field_access():
    Player(name="Pelé", age=80).create()
    Player(name="Maradona", age=60).create()

    players = list(Player.find({Player.name: "Pelé"}))
    assert len(players) == 1
    assert players[0].name == "Pelé"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_id_transformation_with_field_access():
    player = Player(name="Pelé", age=80).create()
    Player(name="Maradona", age=60).create()

    player = Player.find_one({Player.id: player.id})
    assert player.name == "Pelé"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_get_with_field_access():
    Player(name="Pelé", age=80).create()

    player = Player.get({Player.name: "Pelé"})
    assert player.name == "Pelé"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_find_one_with_field_access():
    Player(name="Pelé", age=80).create()

    player = Player.find_one({Player.name: "Pelé"})
    assert player is not None
    assert player.name == "Pelé"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_afind_with_field_access():
    await Player(name="Pelé", age=80).acreate()
    await Player(name="Maradona", age=60).acreate()

    players = []
    async for player in Player.afind({Player.name: "Pelé"}):
        players.append(player)

    assert len(players) == 1
    assert players[0].name == "Pelé"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_aget_with_field_access():
    await Player(name="Pelé", age=80).acreate()

    player = await Player.aget({Player.name: "Pelé"})
    assert player.name == "Pelé"


@pytest.mark.usefixtures(ASYNC_INIT_CONFIG)
async def test_afind_one_with_field_access():
    await Player(name="Pelé", age=80).acreate()

    player = await Player.afind_one({Player.name: "Pelé"})
    assert player is not None
    assert player.name == "Pelé"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_embedded_field_access():
    User(name="John", address=Address(city="New York", zip_code=10001)).create()

    # Test accessing embedded field
    # Assuming the syntax for embedded field access is Parent.child.grandchild
    # If the current implementation supports it.
    # Based on the user request, they want to add test for embedding object as well.
    # If the library doesn't support `User.address.city`, we might need to implement it or test the dict way if that's what's supported.
    # But the user asked to "add test for all kind of retreive like find, afind, get, aget etc. Also make sure to add test for embedding object as well if posible."
    # The current implementation of `__getattr__` in `ODMMeta` (in models.py) seems to return the name of the field.
    # It doesn't seem to return a field object that supports further dot access for embedded fields yet.
    # However, let's check if `User.address` returns "address".

    assert User.address == "address"

    # For embedded fields, usually we want something like "address.city".
    # If the current implementation doesn't support `User.address.city`, we can't test it directly as `User.address.city`.
    # But we can test that we can query using the string "address.city".

    user = User.get({"address.city": "New York"})
    assert user.name == "John"


def test_field_access_with_defaults():
    class Item(Document):
        name: str = "default_name"
        price: int = Field(default=100)

    assert Item.name == "name"
    assert Item.price == "price"


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_one_with_field_access():
    Player(name="Ronaldo", age=25).create()

    # Test update_one with field access in filter and data
    result = Player.update_one(
        filter={Player.name: "Ronaldo"}, data={"$set": {Player.age: 26}}
    )
    assert result.modified_count == 1

    player = Player.get({Player.name: "Ronaldo"})
    assert player.age == 26


@pytest.mark.usefixtures(INIT_CONFIG)
def test_update_many_with_field_access():
    Player(name="Messi", age=34).create()
    Player(name="Messi", age=30).create()

    # Test update_many
    result = Player.update_many(
        filter={Player.name: "Messi"}, data={"$set": {Player.age: 25}}
    )
    assert result.modified_count == 2

    count = Player.count_documents({Player.age: 25})
    assert count == 2


@pytest.mark.usefixtures(INIT_CONFIG)
def test_delete_one_with_field_access():
    Player(name="Neymar", age=29).create()

    # Test delete_one
    result = Player.delete_one({Player.name: "Neymar"})
    assert result.deleted_count == 1

    assert Player.count_documents({Player.name: "Neymar"}) == 0


@pytest.mark.usefixtures(INIT_CONFIG)
def test_delete_many_with_field_access():
    Player(name="Mbappe", age=22).create()
    Player(name="Mbappe", age=23).create()

    # Test delete_many
    result = Player.delete_many({Player.name: "Mbappe"})
    assert result.deleted_count == 2

    assert Player.count_documents({Player.name: "Mbappe"}) == 0
