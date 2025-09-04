# Find and Filter

## Insert Some Data

We will work on the existing Player model.

Let's create some data in the database `test_db` and a collection `player`.

```python
# Code omitted above

{!./docs_src/tutorial/find_and_filter/tutorial000.py[ln:7-37]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_and_filter/tutorial000.py!}
```
</details>

The data will look like

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
...
```

The `rating` field should be set as an index in the database as we set it as an index in `ODMConfig`.

We will continue from the last code that we used to create some data.

## Find data

### Find Data Using MongoDB Console

Let's read the `player` collection using the **MongoDB console**.

```bash
use test_db

db.player.find()
```

Run the above code in the MongoDB console. We should get all the data that was previously created.

### Find Data With MongoDB-ODM

We will use the `find` method of the Player class that is implemented in the `Document` class.

```python
# Code omitted above

{!./docs_src/tutorial/find_and_filter/tutorial000.py[ln:40-44]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_and_filter/tutorial000.py!}
```
</details>

In the `read_players` function, we call the `find` method.

The `find` is a `classmethod` that will return a generator. We will be able to iterate over the generator by using a loop.

We can also use the `next` function like `next(players)`. But `next(players)` may raise an error if there is no data in the `player` collection.

Then we iterate through `players`.

Each object in `players` is equivalent to a `Player` object. And we should get all the functionality of the `Player` class.

Check the console after executing the function.

```bash
Player(id=ObjectId('id'), name='Pelé', country_code='BRA', rating=98, _id=ObjectId('id'))
Player(id=ObjectId('id'), name='Diego Maradona', country_code='ARG', rating=97, _id=ObjectId('id'))
Player(id=ObjectId('id'), name='Zinedine Zidane', country_code='FRA', rating=94, _id=ObjectId('id'))
...
```

For each object, we should get **type hints** that are provided by standard Python and **Pydantic**.

## Accessing data from the returned object

To access values from the object we will use the `.` operator. Nothing special, just standard Python.

Example:

```python
id = player._id
name = player.name
country_code = player.country_code
rating = player.rating
```

## Filter data

We will filter all players where the `rating` is greater than or equal to 10.

### Filtering Data Using MongoDB Console

Let's filter the player collection using the MongoDB console.

```bash
use test_db

db.player.find({"rating": {"$gte": 10}})
```

After executing the above bash code in the MongoDB console, we should get all players who have a rating greater than or equal to 10.

### Filter Data with MongoDB-ODM

We will use the same `find` method of the `Player` class that we used previously to read all data.

The `find` method accepts several arguments like a `filter`, `sort`, `limit`, etc.

```python
# Code omitted above

{!./docs_src/tutorial/find_and_filter/tutorial000.py[ln:47-51]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_and_filter/tutorial000.py!}
```
</details>

!!!warning
There is no validation of **JSON** objects. So make sure every keyword is correct. And double-check spelling mistakes.

The `find` class method will return an iterator.

The returned data should be the same as the returned data in **MongoDB Console**.

Check the console after executing the code.

```bash
Player(id=ObjectId('id'), name='Lionel Messi', country_code='ARG', rating=91, _id=ObjectId('id'))
Player(id=ObjectId('id'), name='Kylian Mbappé', country_code='FRA', rating=91, _id=ObjectId('id'))
Player(id=ObjectId('id'), name='Miroslav Klose', country_code='GER', rating=91, _id=ObjectId('id'))
...
```

## Read data with projection

Sometimes we need to limit some fields that should not be pulled from the database to improve network performance. For example, we have a description field that has a very long string but on the list page, we don't need to pull it.

In that scenario, we can use `projection` kwargs in the `find` function to limit the data pulling.

In this example, we eliminate the `rating` field while getting data from the database.

```python
# Code omitted above

{!./docs_src/tutorial/find_and_filter/tutorial000.py[ln:54-58]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_and_filter/tutorial000.py!}
```
</details>

Check the console after executing the code.

```bash
Player(id=ObjectId('id'), name='Zinedine Zidane', country_code='FRA', rating=None, _id=ObjectId('id'))
Player(id=ObjectId('id'), name='Ronaldo', country_code='BRA', rating=None, _id=ObjectId('id'))
Player(id=ObjectId('id'), name='Lionel Messi', country_code='ARG', rating=None, _id=ObjectId('id'))
...
```

!!!warning
    We need to pull all fields that are required. We can only eliminate `optional` or `nullable` fields. If we do not pull a field, then the field value will be the default value.

## Learning Curve

Filtering data is a crucial part of most DBMS systems.

To filter data from a database, every developer should know how a particular database provides the filtering API.

Also, when we add an extra modeling system for a better developer experience, things get more complicated. Then developers should know both the filtering system (database way and model way). But we won't do that here.

MongoDB already has a broad JSON query system. We will use that directly.

So no complex query learning curve was added to the learning process. We will filter data the MongoDB way.
