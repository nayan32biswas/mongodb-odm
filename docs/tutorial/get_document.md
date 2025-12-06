# Get Document

### Database

We will start with the same database structure and the same amount of data as previously.

## Get First Document

Sometimes we need to get one object. In that scenario, we will use the classmethod `get`.

The `get` is a classmethod that returns a single object.

The method will raise an error if no document exists.

The exception type will be `ObjectDoesNotExist`, inherited from Python's `Exception`. Import `ObjectDoesNotExist` from `mongodb_odm.exceptions`.

```python
# Code omitted above

{!./docs_src/tutorial/get_document/tutorial000.py[ln:53-58]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/get_document/tutorial000.py!}
```
</details>

If the filter matches the collection data, then it will return a `Player` type object.

## Get Last Document

To find the **last** document from the collection we also use `find_last`.

```python
# Code omitted above

{!./docs_src/tutorial/get_document/tutorial000.py[ln:61-64]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/get_document/tutorial000.py!}
```
</details>

The `get` method accepts the sort kwargs argument. The `sort` kwargs accepts several types of data.

The data type is `Union[str, Sequence[tuple[str, Union[int, str, Mapping[str, Any]]]]]`.
