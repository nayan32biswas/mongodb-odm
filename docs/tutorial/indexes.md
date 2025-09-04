# Indexes

## Intro

Indexing is very important for a database. Indexes support the efficient execution of queries in MongoDB. Indexing itself is a very broad topic. Here we won't be discussing how indexes work and what the benefits are.

In this chapter, we will discuss how we can manage indexes using `MongoDB-ODM`.

Please visit the <a href="https://www.mongodb.com/docs/manual/indexes/" class="external-link" target="_blank">Indexes</a> section in MongoDB Documentation to learn more about how indexes work in MongoDB.

## Define indexes in MongoDB-ODM

To create indexes we will define the `indexes` field in the `ODMConfig` class.

We declare the `indexes` field with the class `IndexModel` that is imported from `mongodb_odm`. But `IndexModel` is directly imported from <a href="https://pymongo.readthedocs.io/en/stable/" class="external-link" target="_blank">PyMongo</a>. Visit the PyMongo <a href="https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html?highlight=IndexModel#pymongo.collection.Collection.create_indexes" class="external-link" target="_blank">create_indexes doc</a> for details.

```Python hl_lines="4 13-15"
{!./docs_src/tutorial/indexes/tutorial000.py[ln:1-15]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/indexes/tutorial000.py!}
```
</details>

We define indexes in our model in the `ODMConfig` class.

## Create indexes

To create indexes in our database we will use the `apply_indexes` function.

We import `apply_indexes` from `mongodb_odm`.

```Python hl_lines="4 25"
{!./docs_src/tutorial/indexes/tutorial000.py!}
```

We define indexes in our model. But indexes won't be affected or created until we explicitly call `apply_indexes`.

Call the `apply_indexes` function to create indexes in the database.

## Update Indexes

We add some changes in the index definition.

```Python hl_lines="4 12-15 25"
{!./docs_src/tutorial/indexes/tutorial001.py!}
```

We made a simple change to check the update mechanism. We changed `ASCENDING` to `DESCENDING` index for `country_code`.

Let's look at the database and select the indexes tab for the `player` collection.

We should see two indexes. `_id` is the default index created by MongoDB and `country_code_1` is the newly created index.

<img class="shadow" src="/img/tutorial/indexes/image000.png">

The `country_code_1` is created as an index field in the `player` collection and the field should be unique as we defined in `ODMConfig` and also reflected in the index property as **UNIQUE**.

## Configure CLI

Make sure the `apply_indexes` function is called after configuring the connection. We can configure the `CLI` to call `apply_indexes`.

It's recommended to use the <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a> package to call `apply_indexes` from `CLI`.
