# Foreign Key Relationship Intro

## Foreign Key Relation

We added new `Country` model that has relation with `Player` model.

To create relation with `Player` model we need to use `ODMObjectId` as data type, that imported from `mongodb_odm`.

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
MongoDB does not manage or validate relation between collection. We have to manage that data by ourself. We are assigning foreign key with **ODMObjectId**.

First import `ODMObjectId` from `mongodb_odm`.

`ODMObjectId` has the complete functionality of `ObjectId` from bson package. `ODMObjectId` was directly inherited from `ObjectId` and added a validation function to work with **Pydantic**.

### Relationship

From `Player` model we declare `country_id` which is `ODMObjectId` type object. The `country_id` field only hold `_id` from country document.

Here we define a logical field `country`. The `country` field don't have any action in database.

The `Relationship` accept multiple field one of them is `local_field` and it's required. The `local_field` field will define the local field that are related with.

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

In this example, we will create some player that has a relation with the country collection.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py[ln:34-38]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/foreignkey_relationship/tutorial000.py!}
```
</details>

First we clear all data for collection `Country` and `Player`.

Then we create a document for `Country`.

After that, we create two players in the database that has a relation with the country document.

## Read Data

Here we read all player from database. But country field will not have `Country` object since we don't read it from database.

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

The `load_related` is a classmethod that load all or partially related field all allocate them with related fields.

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

The printed data display again with pretty formatted.

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
    If we call `load_related` the data will be loaded immediately no lazy loading will be applied.

### Read related data of specific field

By default, `load_related` will load all related data from the database.

We can narrow down what relational document will be loaded from the database by passing a list of the field name in `fields` if we don't need all.

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

We can load related data for single objects also.

In this example, we provide two approaches to load-related data.

In approach one we use the general method.

In approach two we use classmethod `load_related` to load-related data.

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
