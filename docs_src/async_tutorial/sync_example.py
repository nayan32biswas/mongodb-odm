import os

from mongodb_odm import Document, Field, apply_indexes, connect, disconnect

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb")


class User(Document):
    name: str = Field()
    email: str = Field()


def main():
    # Connection
    connect(MONGO_URL)
    apply_indexes()

    # Create document
    user = User(name="John", email="john@example.com")
    user.create()

    # Find documents
    _users = list(User.find({"name": "John"}))

    # Update document
    user.update({"$set": {"name": "Jane"}})

    # Delete document
    user.delete()

    # Cleanup
    disconnect()


if __name__ == "__main__":
    main()
