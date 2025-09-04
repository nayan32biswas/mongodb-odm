# Update

We will work on the existing Player model.

Let's create some data in the database `test_db` and a collection `player`.

```python
# Code omitted above

{!./docs_src/tutorial/update/tutorial000.py[ln:7-37]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/update/tutorial000.py!}
```
</details>

## Update Document

Let's get one player from the database and update its rating to `97`.

```python
# Code omitted above

{!./docs_src/tutorial/update/tutorial000.py[ln:45-48]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/update/tutorial000.py!}
```
</details>

Here first we pull the player document from the database with the name `Pelé`.

And set his `player.rating = None`.

Then update the full document by calling `player.update()`.

The method `.update()` will get all data from the player object and update one document filtered by that player's `_id`. All data will be updated that is assigned with the model.

## Update One Document

In certain scenarios, we need to update a single small number of fields instead of full documents and need to improve the network bandwidth. In that case, or any other case, we need to update one document.

Here we can use the `update_one` classmethod to update data.

```python
# Code omitted above

{!./docs_src/tutorial/update/tutorial000.py[ln:51-55]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/update/tutorial000.py!}
```
</details>

The `update_one` classmethod accepts the filter object in the first argument with the kwargs `filter`. It accepts data as the second argument.

A maximum of one document will be updated.

!!! warning
    This function does not validate data with the data model. So make sure you follow the data type that defines in the data model. Otherwise, we will get data validation errors in the future.

## Update Many Document

To update multiple documents, we will use the classmethod `update_many`.

```python
# Code omitted above

{!./docs_src/tutorial/update/tutorial000.py[ln:58-60]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/update/tutorial000.py!}
```
</details>

It accepts the arguments like `update_one`.

But as the name suggests, it will update multiple documents.

!!! warning
    As with `update_one`, this function does not validate data with the data model. So make sure you follow the data type that defines in the data model.
