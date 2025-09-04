# Foreign Key Relationship Intro

## Foreign Key Relation

We added a new `Country` model that has a relationship with the `Player` model.

To create a relationship with the `Player` model, we need to use `ODMObjectId` as the data type, which is imported from `mongodb_odm`.

```Python hl_lines="8 15 19"
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py[ln:1-29]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py!}
```
</details>

!!! tip
    MongoDB does not manage or validate relationships between collections. We have to manage that data ourselves. We are assigning a foreign key with **ODMObjectId**.

First import `ODMObjectId` from `mongodb_odm`.

`ODMObjectId` has the complete functionality of `ObjectId` from the bson package. `ODMObjectId` was directly inherited from `ObjectId` and added a validation function to work with **Pydantic**.

### Relationship

From the `Player` model we declare `country_id` which is an `ODMObjectId` type object. The `country_id` field only holds the `_id` from the country document.

Here we define a logical field `country`. The `country` field doesn't have any action in the database.

The `Relationship` accepts multiple fields, one of them is `local_field` and it's required. The `local_field` field will define the local field that is related to.

```Python hl_lines="9 24"
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py[ln:1-29]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py!}
```
</details>

## Insert Player

In this example, we will create some players that have a relationship with the country collection.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py[ln:37-41]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py!}
```
</details>

First we clear all data from the `Country` and `Player` collections.

Then we create a document for `Country`.

After that, we create two players in the database that have a relationship with the country document.

## Read Data

Here we read all players from the database. But the country field will not have a `Country` object since we don't read it from the database.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py[ln:44-47]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py!}
```
</details>

## Load Related Field

### Read data with related field

In this example, we will read all players with their related countries.

To read related countries we will use an extra class method `load_related`.

The `load_related` is a classmethod that loads all or partially related fields and allocates them with related fields.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py[ln:50-54]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py!}
```
</details>

After running the `read_data_with_related_field` function two objects will be printed with related data `country`.

```bash
Player(id=ObjectId('id'), name='Jamal Bhuyan', country_id=ObjectId('id'), rating=None, country=Country(id=ObjectId('id'), name='Bangladesh', _id=ObjectId('id')), _id=ObjectId('id'))
Player(id=ObjectId('id'), name='Mohamed Emon Mahmud', country_id=ObjectId('id'), rating=None, country=Country(id=ObjectId('id'), name='Bangladesh', _id=ObjectId('id')), _id=ObjectId('id'))
```

The printed data is displayed again with pretty formatting.

```python
Player(
    id=ObjectId("id"),
    name="Jamal Bhuyan",
    country_id=ObjectId("id"),
    rating=None,
    country=Country(
        id=ObjectId("id"),
        name="Bangladesh",
        _id=ObjectId("id"),
    ),
    _id=ObjectId("id"),
)
Player(
    id=ObjectId("id"),
    name="Mohamed Emon Mahmud",
    country_id=ObjectId("id"),
    rating=None,
    country=Country(
        id=ObjectId("id"),
        name="Bangladesh",
        _id=ObjectId("id"),
    ),
    _id=ObjectId("id"),
)
```

!!!warning
    If we call `load_related`, the data will be loaded immediately; no lazy loading will be applied.

### Read related data of specific field

By default, `load_related` will load all related data from the database.

We can narrow down which relational documents will be loaded from the database by passing a list of field names in `fields` if we don't need all of them.

In this example, we pass the `country` field that needs to be loaded from the database.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py[ln:57-61]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py!}
```
</details>

After running the `read_related_data_of_specific_field` function the output will be the same as the previous function since we don't have multiple related fields.

### Load Related for Single Object

We can also load related data for single objects.

In this example, we provide two approaches to load related data.

In approach one, we use the general method.

In approach two, we use the classmethod `load_related` to load related data.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py[ln:64-75]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py!}
```
</details>

The printed data from the two methods will be identical.

Also, the two methods are functionally almost identical.
