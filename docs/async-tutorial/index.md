# Async/Await Support

MongoDB-ODM now provides comprehensive support for async/await operations, built on top of PyMongo's async capabilities. This enables you to build high-performance asynchronous applications with MongoDB while maintaining the familiar ODM interface.

## Async Await Features

We've added async/await support to MongoDB-ODM with the following key features:

### Async Function Naming Convention

- Most of the async methods are prefixed with `a` and aligned with existing methods (e.g., `find()` → `afind()`, `create()` → `acreate()`).
- Function arguments remain the same between sync and async versions
- Consistent API design makes migration straightforward

### Backward Compatibility

- All existing synchronous functionality remains unchanged
- No breaking changes to current sync operations
- You can gradually migrate to async operations

### Complete Async Coverage

- All major database operations have async equivalents
- Connection management, CRUD operations, aggregation, transactions
- Index management and relationship loading

## Quick Example

Here's a simple comparison showing the similarity between sync and async operations:

### Synchronous (Existing)

```Python
{!./docs_src/async_tutorial/sync_example.py!}
```

### Asynchronous (New)

```Python
{!./docs_src/async_tutorial/async_example.py!}
```

## Key Async Methods

All async methods follow the same pattern - they're prefixed with `a` and require `await`:

### Connection

- `connect(..., async_is_enabled=True)` - Enable async mode
- `await adisconnect()` - Close async connection
- `await adrop_database()` - Drop database asynchronously

### Index Management

- `await async_apply_indexes()` - Apply indexes asynchronously

### Operations

- `await doc.acreate()` - Create document
- `Model.afind(filter)` - Find documents (returns AsyncIterator)
- `await Model.afind_one(filter)` - Find single document
- `await Model.aget(filter)` - Get document (raises if not found)
- `await Model.aget_or_create(filter, **data)` - Get or create document
- `await doc.aupdate(data)` - Update document
- `await Model.aupdate_one(filter, data)` - Update one document
- `await Model.aupdate_many(filter, data)` - Update multiple documents
- `await doc.adelete()` - Delete document
- `await Model.adelete_one(filter)` - Delete one document
- `await Model.adelete_many(filter)` - Delete multiple documents
- `await Model.acount_documents(filter)` - Count documents
- `await Model.aexists(filter)` - Check if documents exist
- `Model.aaggregate(pipeline)` - Aggregation (returns AsyncIterator)
- `await Model.aget_random_one(filter)` - Get random document
- `await Model.abulk_write(operations)` - Bulk operations
- `await Model.aload_related(objects, fields)` - Load relationships

### Sessions & Transactions

- `await Model.astart_session()` - Start async session for transactions

## Troubleshooting

### Event loop synchronization issues

When using async functions in environments where an event loop is already running (like Jupyter notebooks, some web frameworks, or testing environments), you may encounter `RuntimeError: asyncio.run() cannot be called from a running event loop`. This happens because `asyncio.run()` tries to create a new event loop, but one already exists.

The solution is to detect if an event loop is running and handle it appropriately:

```py
def run_async(func_call: Coroutine[Any, Any, T]) -> T:
    """
    Run an async function, handling both cases where an event loop
    is already running or not.
    """
    try:
        # Check if we're already in an event loop
        asyncio.get_running_loop()
        # If we are, run in a separate thread to avoid conflicts
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, func_call)
            return future.result()
    except RuntimeError:
        # No event loop running, safe to use asyncio.run()
        return asyncio.run(func_call)


def create_indexes() -> None:
    run_async(async_apply_indexes())
```
