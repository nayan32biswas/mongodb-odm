# Initiate Database and Define Model

## Initiate Database and Create Collection

There is no need to create a database or collection separately. MongoDB automatically creates a new database and collection while we insert new data.

You need to define a Pydantic model that should inherit **Document** from mongodb_odm.
When new insertion takes place, MongoDB automatically creates everything if something does not exist.

## Target

- First, we will create a Player Document model class.
- Define indexes.
- Make sure everything is working and has an impact on the database.

Here's a collection structure that we want to achieve.

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

## Create the Document Model Class

The first thing we need to do is create a class to represent the data in the collection.

```Python
{!./docs_src/tutorial/init_and_define_model/tutorial000.py[ln:1-9]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/init_and_define_model/tutorial000.py!}
```
</details>

Import `Document` from `mongodb_odm`. Define the `Player` model that should use `Document` as the parent class.

## Define the collections and fields

The next step is to define the fields of the class by using standard Python type annotations.

The name of each of these variables will be the name of the field in the collection. And the type of each of them will also be the type of collection field.

```Python hl_lines="1-3 7-9"
{!./docs_src/tutorial/init_and_define_model/tutorial000.py[ln:1-9]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/init_and_define_model/tutorial000.py!}
```
</details>

### Field declaration

- Start with the field `name` defined as type str, which is the standard way to declare something with type in Python.
- We declare `country_code` with type `str` and in our database it will be stored as a `string` type.
- In the end, we define `rating`. Notice that it has a type of `Optional[int]`. And we import that `Optional` from the `typing` standard module. The `rating` field can be `null` or `int` in the database.

### Primary key

- You may notice we did not define the primary key.
- We use MongoDB default primary key `_id` as our primary key.
- You can access `id` and `_id (PrivateAttr)` both should share the same value.

### Model ODMConfig

The `ODMConfig` class inside the `Player` is a special class.

We will use this `ODMConfig` class to change the configuration of the `Player` class.

```Python hl_lines="11"
{!./docs_src/tutorial/init_and_define_model/tutorial000.py!}
```

## Custom Collection Name

By default, the collection name of the `Player` model will be **player**. The model name will be converted to **snake case**.

But we can customize the default behavior by defining `collection_name` in the `ODMConfig` class.

```Python hl_lines="12"
{!./docs_src/tutorial/init_and_define_model/tutorial000.py!}
```
