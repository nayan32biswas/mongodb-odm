# Create

Here's a reminder of how the collection would look like, this is the data we want to add:

```js
{
  "_id": ObjectId('id'),
  "name": "Pelé",
  "country_code": "BRA",
  "rating": null
}
{
  "_id": ObjectId('id'),
  "name": "Diego Maradona",
  "country_code": "ARG",
  "rating": 97
}
{
  "_id": ObjectId('id'),
  "name": "Zinedine Zidane",
  "country_code": "FRA",
  "rating": 96
}
```

## Define Model

We will continue from where we left off in the [Initiate Database and Define Model](./init_and_define_model.md) Chapter.

```{.python .annotate}
{!./docs_src/tutorial/create/tutorial000.py[ln:1-10]!}

# Code omitted below
```

{!./docs_src/tutorial/create/annotations/en/tutorial000.md!}

## Create data with MongoDB console

Let's create the `player` collection in `test_db` and insert one player record using the **MongoDB console**.

```shell
use test_db
db.player.insertOne({
    "name": "Pelé",
    "country_code": "BRA",
    "rating": null,
})
```

### Explore MongoDB database

Let's check the MongoDB database and find the `player` collection in the `test_db` database.

The collection should have one item on the list.

```js
{
  "_id": ObjectId('id'),
  "name": "Pelé",
  "country_code": "BRA",
  "rating": null
}
```

## Set database connection

Set the database connection once for a project. It's recommended to set up a connection while the project is initializing.

```{.python .annotate hl_lines="4"}
# Code omitted above

{!./docs_src/tutorial/create/tutorial000.py[ln:24-27]!}

# Code omitted below
```

{!./docs_src/tutorial/create/annotations/en/tutorial000.md!}

## Create data with MongoDB-ODM

Create two players using `MongoDB-ODM`.

We use the `create_documents` function to create two players.

First, we create players at declaration time.

Second, we assign a player object to `maradona`. Then we create/insert the data into the database by calling the `create` method.

```{.python .annotate}
# Code omitted above

{!./docs_src/tutorial/create/tutorial000.py[ln:13-21]!}

# Code omitted below
```

{!./docs_src/tutorial/create/annotations/en/tutorial000.md!}

Sometimes we need to assign an object and then change some data and insert the data at the end. In that case, use the second approach. First, assign the object, do all necessary changes, and save the document later.

### Impact in Database

After running the file, we should find the two player documents in the `player` collection of the `test_db` database.

## Full file code

```{.python .annotate}
{!./docs_src/tutorial/create/tutorial000.py!}
```

{!./docs_src/tutorial/create/annotations/en/tutorial000.md!}
