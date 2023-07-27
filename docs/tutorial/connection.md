# Manage Database Connection

## Set db connection

Set database connection one time for a project.

```python
from mongodb_odm import connect

connect(os.environ.get("MONGO_URL", "mongodb://localhost:27017/testdb"))
```

It's recommended to set a connection one time for the project.

**MongoDB-ODM** will memorize your connection string and manage your database connectivity behind the scene, using <a href="https://pymongo.readthedocs.io/en/stable/" class="external-link" target="_blank">PyMongo</a>.

## Disconnect the connection

To disconnect the database connection we will use the `disconnect` function from `mongodb_odm`.

```python
from mongodb_odm import disconnect

disconnect()
```

The `disconnect` function will close the existing connection client. And remove provided **connection URL**.

## Multiple Database

Visit the [Multiple Database Chapter](../advanced-tutorial/multiple-database.md) to learn how to implement multiple database features.
