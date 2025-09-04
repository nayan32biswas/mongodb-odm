# Async/Await API Reference

Complete reference for all async methods in MongoDB-ODM. All async methods are prefixed with `a` and require `await`.

## Connection Management

**connect()** - Establish async connection

```python
connect(url: str, async_is_enabled=True) -> AsyncMongoClient
```

**adisconnect()** - Close async connection

```python
await adisconnect() -> bool
```

**adrop_database()** - Drop database asynchronously

```python
await adrop_database(database: Optional[str] = None) -> None
```

## Document Operations

### Instance Methods

**acreate()** - Create document

```python
await doc.acreate(**kwargs) -> Self
```

**aupdate()** - Update document

```python
await doc.aupdate(raw: Optional[dict] = None, **kwargs) -> UpdateResult
```

**adelete()** - Delete document

```python
await doc.adelete(**kwargs) -> DeleteResult
```

### Query Methods

**afind()** - Find documents with async iteration

```python
Model.afind(filter=None, projection=None, sort=None, skip=None, limit=None) -> AsyncIterator[Self]

# Usage
async for doc in Model.afind({"status": "active"}):
    print(doc.name)
```

**afind_one()** - Find single document

```python
await Model.afind_one(filter=None, projection=None, sort=None) -> Optional[Self]
```

**aget()** - Get document (raises if not found)

```python
await Model.aget(filter: dict, sort=None) -> Self
```

**aget_or_create()** - Get or create document

```python
await Model.aget_or_create(filter: dict, **kwargs) -> tuple[Self, bool]
```

### Update Methods

**aupdate_one()** - Update single document

```python
await Model.aupdate_one(filter: dict, data: dict) -> UpdateResult
```

**aupdate_many()** - Update multiple documents

```python
await Model.aupdate_many(filter: dict, data: dict) -> UpdateResult
```

### Delete Methods

**adelete_one()** - Delete single document

```python
await Model.adelete_one(filter: dict) -> DeleteResult
```

**adelete_many()** - Delete multiple documents

```python
await Model.adelete_many(filter: dict) -> DeleteResult
```

### Count & Existence

**acount_documents()** - Count documents

```python
await Model.acount_documents(filter=None) -> int
```

**aexists()** - Check if documents exist

```python
await Model.aexists(filter=None) -> bool
```

## Advanced Operations

**aaggregate()** - Run aggregation pipeline

```python
Model.aaggregate(pipeline: list, get_raw=False) -> AsyncIterator[Any]

# Usage
async for result in Model.aaggregate([{"$match": {"status": "active"}}]):
    print(result)
```

**aget_random_one()** - Get random document

```python
await Model.aget_random_one(filter=None) -> Self
```

**abulk_write()** - Bulk operations

```python
await Model.abulk_write(requests: Sequence[WriteOp]) -> BulkWriteResult
```

**aload_related()** - Load relationships

```python
await Model.aload_related(object_list: AsyncIterator[Self], fields=None) -> Sequence[Self]
```

## Session Management

**astart_session()** - Start async session

```python
await Model.astart_session() -> AsyncClientSession

# Usage
async with await Model.astart_session() as session:
    async with session.start_transaction():
        await Model.aupdate_one({"_id": "1"}, {"$inc": {"balance": -100}}, session=session)
```

## Index Management

**async_apply_indexes()** - Apply indexes asynchronously

```python
await async_apply_indexes() -> None
```
