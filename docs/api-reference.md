# API Reference

## Intro

In this tutorial section, we will know everything in great detail.

Sometimes we need to check a function or variable as a prompt.

In this section, we will try to create a cheat sheet for quick checkups.

## Insert Some Data

```python
{!./docs_src/reference/tutorial000.py!}
```

## Definition of Model Class

### Class

## Config

In the Config class, we already set some default values to change class behavior.

```python
    class Config(BaseModel.Config):
        orm_mode: bool = True
        allow_population_by_field_name: bool = True
        collection_name: Optional[str] = None
        allow_inheritance: bool = False
        index_inheritance_field: bool = True
```

Other than these values, we use `BaseModel.Config` value as default from `pydantic`.

- `orm_mode` type `bool` default `True`
- `allow_population_by_field_name` type `bool` default `True`
- `collection_name` type optional `Optional[str]` default `None`
- `allow_inheritance` type `bool` default `False`
- `index_inheritance_field` type `bool` default `True`

## Types

### Sort Type

We will use this `SORT_TYPE` in all of our sorting arguments.

```python
SORT_TYPE = Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]]
```

## Class Method

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

The `create` method does not accept any **MongoDB-ODM** related argument. It's kwargs directly send to the **Pymongo** function.

### find_raw

```python
@classmethod
def find_raw(cls, filter: dict = {}, projection: dict = {}, **kwargs) -> Cursor:
```

The `find_raw` is a special function that returns **Pymongo** find the cursor.

### find

```python
@classmethod
def find(
    cls,
    filter: dict = {},
    sort: Optional[SORT_TYPE] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    projection: dict = {},
    **kwargs,
) -> Iterator[Self]:
```

#### Parameter

The `find_one` classmethod accepts 6 parameters.

1. **filter** was the key for parameter 1. The data type should be `dict` and the default value was `{}`.
2. **sort** was the key for parameter 2. The data type should be `Optional[SORT_TYPE]` and the default value was `None`.
3. **skip** was the key for parameter 3. The data type was `Optional[int]` and the default value was `None`.
4. **limit** was the key for parameter 3. The data type was `Optional[int]` and the default value was `None`.
5. **projection** was the key for parameter 1. The data type should be `dict` and the default value was `{}`.
6. Lastly, it accepts `**kwargs`

#### Return Type

It's `Iterator[Self]`, which is iterable. And we should get type support on each object.

### find_one

```python
@classmethod
def find_one(
    cls,
    filter: dict = {},
    projection: dict = {},
    sort: Optional[SORT_TYPE] = None,
    **kwargs,
) -> Optional[Self]:
```

#### Received Parameter

The `find_one` classmethod accept 3 parameter.

1. **filter** was the key for parameter 1. The ata type should be `dict` and the default value assigned with `{}`.
2. **projection** was the key for parameter 1. The ata type should be `dict` and the default value was `{}`.
3. **sort** was the key for parameter 2. The ata type should be `Optional[SORT_TYPE]` and the default value assigned with `None`.
4. Lastly, it accepts `**kwargs`

### get

```python
@classmethod
def get(cls, filter: dict, sort: Optional[SORT_TYPE] = None, **kwargs) -> Self:
```

### get_or_create

```python
@classmethod
def get_or_create(
    cls, filter: dict, sort: Optional[SORT_TYPE] = None, **kwargs
) -> Tuple[Self, bool]:
```

### count_documents

```python
@classmethod
def count_documents(cls, filter: dict = {}, **kwargs) -> int:
```

### exists

```python
@classmethod
def exists(cls, filter: dict = {}, **kwargs) -> bool:
```

### aggregate

```python
@classmethod
def aggregate(
    cls, pipeline: List[Any], get_raw=False, inheritance_filter=True, **kwargs
) -> Iterator[Union[dict, ODMObj]]:
```

### get_random_one

```python
@classmethod
def get_random_one(cls, filter: dict = {}, **kwargs) -> Self:
```

### update_one

```python
def update_one(cls, filter: dict = {}, data: dict = {}, **kwargs) -> UpdateResult:
```

### update_many

```python
from pymongo.results import UpdateResult

@classmethod
def update_many(cls, filter: dict = {}, data: dict = {}, **kwargs) -> UpdateResult:
```

### delete_one

```python
@classmethod
def delete_one(cls, filter: dict = {}, **kwargs) -> DeleteResult:
```

### delete_many

```python
@classmethod
def delete_many(cls, filter: dict = {}, **kwargs) -> DeleteResult:
```

### bulk_write

```python
@classmethod
def bulk_write(
    cls, requests: Sequence[_WriteOp[_DocumentType]], **kwargs
) -> BulkWriteResult:
```

Here `_WriteOp` are `DeleteMany, DeleteOne, IndexModel, InsertOne, ReplaceOne, UpdateMany, UpdateOne` imported from `pymongo.operations`.

### load_related

The classmethod `load_related` will load all related fields from the database.

Data will be loaded immediately no leave loading will be applied.

```python
@classmethod
def load_related(
    cls,
    object_list: Union[Iterator[Self], Sequence[Self]],
    fields: List[str] = [],
    **kwargs,
) -> Sequence[Self]:
```

## Method

In this section we will explain every **Method** that are callable after creating the object.

### update

```python
def update(self, raw: dict = {}, **kwargs) -> UpdateResult:
```

### delete

```python
def delete(self, **kwargs) -> DeleteResult:
```