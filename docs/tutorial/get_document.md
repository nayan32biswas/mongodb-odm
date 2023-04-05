# Get Document

### Database

We will start from the same database structure and the same number of data as previously.

## Get First Document

Sometimes we need to get one object. In that scenario, we will use classmethod `get`.

The `get` is a classmethod that returns single object.

The method will raise an error if no document exists.

The exception type will be `ObjectDoesNotExist` inherited from python `Exception`. import `ObjectDoesNotExist` from `mongodb_odm.exceptions`

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

If the filter matched with the collection data then it will return the `Player` type object.

## Get Last Document

To find the **last** document from the collection we also use `find_last`.

```python
# Code omitted above

{!./docs_src/tutorial/get_document/tutorial000.py[ln:61-65]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/get_document/tutorial000.py!}
```
</details>

The `get` method accepts the sort kwargs argument. The `sort` kwargs accept several types of data.


Data type was `Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]]`.
