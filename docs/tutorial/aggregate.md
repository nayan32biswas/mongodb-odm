# Aggregate

Aggregation operations process multiple documents and return computed results. You can use aggregation operations to:

- Group values from multiple documents together.
- Perform operations on the grouped data to return a single result.
- Analyze data changes over time.

## Aggregation Pipelines

An aggregation pipeline consists of one or more stages that process documents:

- Each stage performs an operation on the input documents. For example, a stage can filter documents, group documents, and calculate values.
- The documents that are output from a stage are passed to the next stage.
- An aggregation pipeline can return results for groups of documents. For example, return the total, average, maximum, and minimum values.

Read <a  href="https://www.mongodb.com/docs/manual/aggregation/" class="external-link" target="_blank">MongoDB aggregation</a> for more details about aggregation.

### Database

We will start with the same database structure and the same amount of data as previously.

## Aggregate data using MongoDB Console

```bash
use test_db
db.player.aggregate([{"$group": {"_id": "$country_code", "total_player": {"$sum": 1}}}])
```

The returned data will be:

```bash
{_id: 'ARG', total_player: 3}
{_id: 'BRA', total_player: 3}
{_id: 'ENG', total_player: 3}
...
```

## Aggregate data using MongoDB-ODM

To aggregate over the database we will use the classmethod `aggregate`.

The `aggregate` method will return an `Iterator`.

With `find`, we can't use array index-like access on the returned data. We should loop over the data.

```python
# Code omitted above

{!./docs_src/tutorial/aggregate/tutorial000.py[ln:45-53]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/aggregate/tutorial000.py!}
```
</details>

### Checkout the Console

After executing the function, the console data should look like this:

```bash
ODMObj(_id='ARG', total_player=3)
ODMObj(_id='BRA', total_player=3)
ODMObj(_id='ENG', total_player=3)
...
```

Check that the MongoDB console aggregate and ODM aggregate method are both returning the same data.

### ODMObj type

You may notice that our object has returned a new type of object called `ODMObj`.

When we aggregate something from the database, the returned data can be any type of object.

The **MongoDB-ODM** `aggregate` uses the **PyMongo** `aggregate` function directly. And **PyMongo** `aggregate` returns a dictionary-type iterator.

So we convert the dictionary-like objects to `ODMObj` where we can access data like a model.

We can easily convert `ODMObj` to a python `dict` by calling `.dict()`.
