# Multiple Database

We can work with multiple databases within a single node. There are multiple use cases for multiple database systems. If you want to implement log on a separate database rather than the main database.

## Connection

We learn how to establish the connection with the database in the [connection chapter](../tutorial/connection.md).

To work with multiple databases we will use the same `connect` function that we used previously.

The `connect` function accepts two arguments. The first one is `url` (required str type) and the second one is `databases` (optional set type).

The first argument `url` string should have a **default database**. The second argument `databases` are optional. We can send multiple database names as needed.

```python hl_lines="4-7"
# Code omitted above

{!./docs_src/advanced_tutorial/multiple_database/tutorial000.py[ln:18-23]!}

# Code omitted below
```

## Mode Definition

The no need for any modification of your model which will use the default database.

We will use a **logging** database to store all documents for `Log`. For the `Log` model, we always will use the **logging** database. Modification or document retrieval should have happened in the **logging** database.

Here we define the `Log` model that has a field `database = "logging"` inside the `Config` of the model.

```python hl_lines="7"
# Code omitted above

{!./docs_src/advanced_tutorial/multiple_database/tutorial000.py[ln:11-15]!}

# Code omitted below
```

**Note**: MongoDB does not support **$lookup** with different databases that are also applicable here. We are not permitted to perform **$lookup** with the **default** and **logging** database.
