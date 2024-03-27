
# SQLAlchemy Transaction Context

An extension for sqlalchemy to store the session object in context and simplify the retrieval of the query result.


## Create instance 
```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_tx_context import SQLAlchemyTransactionContext


engine = create_async_engine(...)
db = SQLAlchemyTransactionContext(engine)
```

## Execute query

`SQLAlchemyTransactionContext` contains the following methods for creating queries with execution
through a context session:
- `select`
- `insert`
- `update`
- `delete`
- `union`
- `union_all`
- `exists`

Query will use a session from the context.

```python
async def some_repository_method():
    await db.insert(...).values(...).execute()


async def some_function():
    async with db.transaction() as tx:
        await some_repository_method()
        await tx.rollback() # Record will not be inserted
```


If there is no session in the context, a default session will be created to execute a single query.

```python
async def some_repository_method():
    await db.insert(...).values(...).execute()

async def some_function():
      await some_repository_method()
```


Calling the transaction method inside the session will create a nested transaction.

```python
async def some_function():
    async with db.transaction() as tx1:
        isinstance(tx1, AsyncSession) # True
        async with db.transaction() as tx2:
            isinstance(tx2, AsyncSessionTransaction) # True
```

## Execute query with proxy methods

List of proxy methods added to the request object

Proxy methods for the `AsyncSession` properties:
- `execute`
- `scalar`
- `scalars`

Example:

```python
value = await db.select(...).execute()
```

The same as:

```python
async with async_sessionmaker(engine).begin() as tx:
    result = await tx.execute(select(...))
```

Proxy methods for the `Result` properties:
- `first`
- `all`

Example:
```python
value = await db.select(...).first()
```

The same as:

```python
async with async_sessionmaker(engine).begin() as tx:
    result = await tx.execute(select(...))
    value = result.first()
```

Proxy methods for the `MappingResult` properties:

- `mapped_first`
- `mapped_one`
- `mapped_all`

Example:
```python
value = await db.select(...).mapped_first()
```

The same as:

```python
async with async_sessionmaker(engine).begin() as tx:
    result = await tx.execute(select(...))
    value = result.mappings().first()
```

Proxy method for the `CursorResult`:

- `rowcount`