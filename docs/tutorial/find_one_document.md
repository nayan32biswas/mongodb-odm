# Find One Document

### Database

We will start from the same database structure and the same number of data as previously.

## Find One

Some times we need to find one object. In that scenario, we will use classmethod `find_one`.

The `find_one` is a classmethod that returns a single object or None if the object not exists.

```python
# Code omitted above

{!./docs_src/tutorial/find_one_document/tutorial000.py[ln:52-54]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_one_document/tutorial000.py!}
```
</details>

If the filter matched with the collection data then it will return the `Player` type object. Otherwise, it will return `None`.

The `find_one` will also act as `find_first`.

## Find Last

To **find the** last document from the collection we also use `find_last`.

```python
# Code omitted above

{!./docs_src/tutorial/find_one_document/tutorial000.py[ln:57-59]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_one_document/tutorial000.py!}
```
</details>

The `find_one` method accepts a sort object.

The `sort` kwargs accept several types of data.

The data type for sort was `Union[str, Sequence[tuple[str, Union[int, str, Mapping[str, Any]]]]]`.
