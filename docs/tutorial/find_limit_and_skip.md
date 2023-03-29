# Data Limit and Skip

We can improve data retrieval performance by limiting or skipping data for a big data set.

## Create data to database

```python
# Code omitted above

{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py[ln:23-42]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py!}
```
</details>

## Limit Data

To control how much data should return from the database we will use `limit` kwargs as a parameter in classmethod `find`.


The `limit` is an optional field in `find`. Also limit should be `int` type value.

Here we retrieve **Player** collection with `limit=2`.

We should get maximum of two document printed in console after executing the `limit_data` function.

```python hl_lines="4"
# Code omitted above

{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py[ln:45-49]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py!}
```
</details>

## Skip Data

To **skip** some of the data we will use `skip` kwargs in classmethod `find`.

The type definition for `skip` was `Optional[int]` and the default was `None`.

Here we retrieve the `Player` collection after skipping the first two documents.

After executing the function we should not see the first two objects from the collection.

```python hl_lines="4"
# Code omitted above

{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py[ln:51-56]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py!}
```
</details>

## Combine Skip and Limit

We can combine `skip` and `limit` and pass it to classmethod `find`.

It will work at the same time.

For example, to retrieve the `Player` collection we pass two kwargs `Player.find(skip=3, limit=2)`.

The return object `players` can max have **2** documents and the first **3** documents should skip as `skip=3`

```python hl_lines="4"
# Code omitted above

{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py[ln:59-63]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py!}
```
</details>

## Pagination

Using `skip` and `limit` we can implement pagination.

We can filter and implement pagination at the same time using classmethod `find`.

```python hl_lines="6"
# Code omitted above

{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py[ln:66-72]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_limit_and_skip/tutorial000.py!}
```
</details>
