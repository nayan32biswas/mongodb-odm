# Data Limit and Skip

We can improve data retrieval performance by limiting or skipping data for a big data set.

### Database

We will start with the same database structure and the same amount of data as previously.

## Limit Data

To control how much data should be returned from the database, we will use the `limit` kwargs as a parameter in the classmethod `find`.

The `limit` is an optional field in `find`. Also, the limit should be an `int` type value.

Here we retrieve the **Player** collection with `limit=2`.

We should get a maximum of two documents printed in the console after executing the `limit_data` function.

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

To **skip** some of the data, we will use the `skip` kwargs in the classmethod `find`.

The type definition for `skip` is `Optional[int]` and the default is `None`.

Here we retrieve the `Player` collection after skipping the first two documents.

After executing the function, we should not see the first two objects from the collection.

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

We can combine `skip` and `limit` and pass them to the classmethod `find`.

They will work at the same time.

For example, to retrieve the `Player` collection, we pass two kwargs: `Player.find(skip=3, limit=2)`.

The returned object `players` can have a maximum of **2** documents and the first **3** documents should be skipped as `skip=3`.

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
