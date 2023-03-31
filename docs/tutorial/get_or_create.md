# Get or Create

Let's say we have a model and we don't know if data exists or not. And we need to get data for that model.

## Insert Some Data

We will work on the existing Player model.

Let's create some data in the database test_db and a collection player.

```python
# Code omitted above

{!./docs_src/tutorial/get_or_create/tutorial000.py[ln:7-37]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_and_filter/tutorial000.py!}
```
</details>

## General Process

To achieve that functionality will first try to get the document. If data does not exist then create a document with the same data.

```python
# Code omitted above

{!./docs_src/tutorial/get_or_create/tutorial000.py[ln:45-52]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/get_or_create/tutorial000.py!}
```
</details>

## Using `get_or_create`

We can achieve that functionality with a single function `get_or_create`.

```python
# Code omitted above

{!./docs_src/tutorial/get_or_create/tutorial000.py[ln:55-64]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/get_or_create/tutorial000.py!}
```
</details>

The `get_or_create` will return two values. The first one is the actual object and the second one is a boolean field. Boolean field indicates the object is existing data or newly created.
