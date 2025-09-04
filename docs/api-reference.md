# API Reference

## Intro

In this tutorial section, we will learn everything in great detail.

Sometimes we need to check a function or variable as a reference.

In this section, we will try to create a cheat sheet for quick reference.

## Insert Some Data

```python
{!./docs_src/reference/tutorial000.py!}
```

## Connection

### connect

```python
def connect(url: str, databases: Optional[Set[str]] = None) -> MongoClient[Any]:
```

### disconnect

```python
def disconnect() -> bool:
```

### get_client

```python
def get_client() -> MongoClient[Any]:
```

## Definition of Model Class

### Class

## ODMConfig

In the ODMConfig class, we already set some default values to change class behavior.

```python
    class ODMConfig(BaseModel.ODMConfig):
        collection_name: Optional[str] = None
        allow_inheritance: bool = False
        index_inheritance_field: bool = True
```

- `collection_name` type `Optional[str]` default `None`
- `allow_inheritance` type `bool` default `False`
- `index_inheritance_field` type `bool` default `True`

## Types

### Generic dict Type

We will use this `DICT_TYPE` for all of our generic dict types.

```python
DICT_TYPE = dict[str, Any]
```

### Sort Type

We will use this `SORT_TYPE` in all of our sorting arguments.

```python
SORT_TYPE = Union[str, Sequence[tuple[str, Union[int, str, Mapping[str, Any]]]]]
```

## Class Methods

In this section, we will explain every **Class Method** that is callable from a defined class.

### \_db

```python
@classmethod
def _db(cls) -> str:
```

We can get the collection name by calling `_db`.

### create

```python
def create(self, **kwargs) -> Self:

```

The `create` method does not accept any **MongoDB-ODM** related arguments. Its kwargs are directly sent to the **PyMongo** function.

### find_raw

```python
@classmethod
def find_raw(
    cls,
    filter: Optional[DICT_TYPE] = None,
    projection: Optional[DICT_TYPE] = None,
    **kwargs: Any,
) -> Cursor[Any]:
```

The `find_raw` is a special function that returns a **PyMongo** find cursor.

### find

```python
@classmethod
def find(
    cls,
    filter: Optional[DICT_TYPE] = None,
    projection: Optional[DICT_TYPE] = None,
    sort: Optional[SORT_TYPE] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    **kwargs: Any,
) -> Iterator[Self]:
```

#### Parameters

The `find` classmethod accepts 6 parameters.

1. **filter** - The data type should be `dict` and the default value is `None`.
2. **projection** - The data type should be `dict` and the default value is `None`.
3. **sort** - The data type should be `Optional[SORT_TYPE]` and the default value is `None`.
4. **skip** - The data type is `Optional[int]` and the default value is `None`.
5. **limit** - The data type is `Optional[int]` and the default value is `None`.
6. Lastly, it accepts `**kwargs`

#### Return Type

It returns `Iterator[Self]`, which is iterable. You should get type support on each object.

### find_one

```python
@classmethod
def find_one(
    cls,
    filter: Optional[DICT_TYPE] = None,
    projection: Optional[DICT_TYPE] = None,
    sort: Optional[SORT_TYPE] = None,
    **kwargs: Any,
) -> Optional[Self]:
```

#### find_one Parameters

The `find_one` classmethod accepts 4 parameters.

1. **filter** - The data type should be `dict` and the default value is `None`.
2. **projection** - The data type should be `dict` and the default value is `None`.
3. **sort** - The data type should be `Optional[SORT_TYPE]` and the default value is `None`.
4. Lastly, it accepts `**kwargs`

### get

```python
@classmethod
def get(
    cls,
    filter: DICT_TYPE,
    sort: Optional[SORT_TYPE] = None,
    **kwargs: Any,
) -> Self:
```

### get_or_create

```python
@classmethod
def get_or_create(
    cls,
    filter: DICT_TYPE,
    sort: Optional[SORT_TYPE] = None,
    **kwargs: Any,
) -> tuple[Self, bool]:
```

### count_documents

```python
@classmethod
def count_documents(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> int:
```

### exists

```python
@classmethod
def exists(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> bool:
```

### aggregate

```python
@classmethod
def aggregate(
    cls,
    pipeline: list[Any],
    get_raw: bool = False,
    inheritance_filter: bool = True,
    **kwargs: Any,
) -> Iterator[Any]:
```

### get_random_one

```python
@classmethod
def get_random_one(cls, filter: Optional[DICT_TYPE] = None, **kwargs: Any) -> Self:
```

### update_one

```python
@classmethod
def update_one(
    cls, filter: DICT_TYPE, data: DICT_TYPE, **kwargs: Any
) -> UpdateResult:
```

### update_many

```python
@classmethod
def update_many(
    cls, filter: DICT_TYPE, data: DICT_TYPE, **kwargs: Any
) -> UpdateResult:
```

### delete_one

```python
@classmethod
def delete_one(cls, filter: DICT_TYPE, **kwargs: Any) -> DeleteResult:
```

### delete_many

```python
@classmethod
def delete_many(cls, filter: DICT_TYPE, **kwargs: Any) -> DeleteResult:
```

### bulk_write

```python
@classmethod
def bulk_write(
    cls, requests: Sequence[WriteOp[Any]], **kwargs: Any
) -> BulkWriteResult:
```

Here `WriteOp` is one of the types: `DeleteMany, DeleteOne, IndexModel, InsertOne, ReplaceOne, UpdateMany, UpdateOne` from `pymongo`

### load_related

The classmethod `load_related` will load all related fields from the database.

Data will be loaded immediately; no lazy loading will be applied.

```python
@classmethod
def load_related(
    cls,
    object_list: Union[Iterator[Self], Sequence[Self]],
    fields: Optional[list[str]] = None,
    **kwargs: Any,
) -> Sequence[Self]:
```

## Methods

In this section we will explain every **Method** that is callable after creating the object.

### update

```python
def update(self, raw: Optional[DICT_TYPE] = None, **kwargs: Any) -> UpdateResult:
```

### delete

```python
def delete(self, **kwargs: Any) -> DeleteResult:
```
