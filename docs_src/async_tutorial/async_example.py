import asyncio
import os

from mongodb_odm import Document, Field, adisconnect, async_apply_indexes, connect

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb")


class User(Document):
    name: str = Field()
    email: str = Field()


async def main():
    connect(MONGO_URL, async_is_enabled=True)
    await async_apply_indexes()

    # Create document
    user = User(name="John", email="john@example.com")
    await user.acreate()

    # Find documents
    _users = [user async for user in User.afind({"name": "John"})]

    # Update document
    await user.aupdate({"$set": {"name": "Jane"}})

    # Delete document
    await user.adelete()

    # Cleanup
    await adisconnect()


asyncio.run(main())
