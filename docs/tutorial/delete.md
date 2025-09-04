# Delete

As in the previous example, let's create some data in the database `test_db` and a collection `player`.

```python
# Code omitted above

{!./docs_src/tutorial/delete/tutorial000.py[ln:23-42]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/delete/tutorial000.py!}
```
</details>

## Delete Document

First, we will get the object.

Then call the `delete` method of that object.

```python
# Code omitted above

{!./docs_src/tutorial/delete/tutorial000.py[ln:45-47]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/delete/tutorial000.py!}
```
</details>

The `delete` method should remove that object from the database.

## Delete One Document

With the `delete` method, we have to make two database calls. First, pull data from the database and then call the delete method.

With the use of `delete_one`, we can delete an object with a single database call.

```python
# Code omitted above

{!./docs_src/tutorial/delete/tutorial000.py[ln:50-52]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/delete/tutorial000.py!}
```
</details>

The classmethod `delete_one` accepts a `filter` as the first argument.

The `delete_one` should delete a maximum of one object.

## Delete Many Document

With the help of the classmethod `delete_many`, we can delete multiple documents with a single database call.

```python
# Code omitted above

{!./docs_src/tutorial/delete/tutorial000.py[ln:55-57]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/delete/tutorial000.py!}
```
</details>

After executing the classmethod `delete_many` all players with a rating of 89 should be deleted from the database.
