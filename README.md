# SQLAlchemy Transaction Context

Minimalistic context-local session and transaction controller for SQLAlchemy AsyncSession.

`sqlalchemy-tx-context` provides context-aware session and transaction management using Python’s contextvars,
eliminating the need to pass AsyncSession objects explicitly. Especially useful in code where database access should
be decoupled from explicit session passing - such as service layers or background jobs.

---

## Features

- Context-local session management via `contextvars`, without relying on thread-locals or global session objects.
- Clean `async with` API for managing session and transaction scopes.
- Supports safe nesting of transactions.
- `.execute(...)` automatically creates a session or transaction if none is active (optional fallback).
- Explicit control over how sessions are scoped and reused.

---

## Installation

```shell
pip install sqlalchemy-tx-context
```

---

## Quick Example

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_tx_context import SQLAlchemyTransactionContext

engine = create_async_engine("postgresql+asyncpg://user:pass@host/db")

db = SQLAlchemyTransactionContext(engine)

async def create_user():
    async with db.transaction():
        await db.execute(insert(User).values(name="John"))

async def get_users():
    async with db.session():
        result = await db.execute(select(User))
        return result.scalars().all()
```


## API Reference

---

### Constructor

```python
SQLAlchemyTransactionContext(
    engine: AsyncEngine,
    *,
    default_session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    auto_context_on_execute: bool = False,
    auto_context_force_transaction: bool = False,
)
```

---

### Parameters:

- `engine` - SQLAlchemy `AsyncEngine` instance.
- `default_session_maker` - Optional async session factory. If omitted, uses `async_sessionmaker(engine)`.
- `auto_context_on_execute` - If `True`, allows `.execute()` to run even without an active session
by creating a temporary one.
- `auto_context_force_transaction` - If `True`, `.execute()` always runs inside a transaction when auto context is used.
If `False`, it uses `.session()` for read-only queries (like `Select` or `CompoundSelect`),
and `.transaction()` for everything else, including `Insert`, `Update`, and raw SQL.

---

### Session Methods:

- `session(...) -> AsyncIterator[AsyncSession]` - Enter a new session context, or reuse an existing
one if `reuse_if_exists=True`.
- `transaction(...) -> AsyncIterator[AsyncSession]` - Enter a transactional context.
Will nest if a transaction is already active.
- `new_session(...) -> AsyncIterator[AsyncSession]` - Create a new isolated session, even if another is already active.
Overrides the context for the duration.
- `new_transaction(...) -> AsyncIterator[AsyncSession]` - Create a new transaction in an isolated session.
- `get_session(strict: bool = True) -> AsyncSession | None` - Return the current session from context.
Raises `NoSessionError` if `strict=True` and no session exists.
- `execute(...) -> Result` - Execute a SQLAlchemy `Executable` using the current or temporary context.
Uses the current session if one is active. Otherwise, behavior depends on `auto_context_on_execute` -
a new session or transaction context may be created automatically.

---

## Auto-context Example

```python
# Opens a temporary session or transaction depending on statement type
db = SQLAlchemyTransactionContext(engine, auto_context_on_execute=True)

await db.execute(insert(User).values(name="Alice"))
await db.execute(select(User))
```

---

## Full Example

For a complete working example using PostgreSQL, see
[`example/`](https://github.com/QuisEgoSum/sqlalchemy-tx-context/tree/main/example).
It demonstrates table creation, data insertion, transactional rollback, and querying.

---

## Exceptions

This library defines a few custom exceptions to help catch context-related mistakes:

- `NoSessionError`: Raised when attempting to access or use a session when none is active and fallback is disabled.
- `SessionAlreadyActiveError`: Raised when entering `.session()` while a session is already active 
(unless `reuse_if_exists=True`).
- `TransactionAlreadyActiveError`: Raised when entering `.transaction()` while a transaction is already active 
and nesting is disabled.

---

## Motivation

SQLAlchemy does not provide an out-of-the-box solution for context-local session tracking when working with
`AsyncSession`. Passing sessions around explicitly can make service-layer code verbose and harder to maintain.

The library introduces a lightweight and predictable abstraction that:

- Stores current session in a `ContextVar`.
- Provides safe transactional/session boundaries.
- Exposes a unified `execute(...)` interface.
- Integrates with standard SQLAlchemy models, statements, and engines.

---

## When should you use this?

- You're writing service-layer logic and want to avoid passing `session` explicitly.
- You need nested transactional logic with clean context boundaries.
- You prefer explicit context management over dependency-injected sessions.
- You work with context-local transaction boundaries in background tasks or microservices.
- You need precise control over session lifecycle and scope.

This library is best suited for functional or script-style code where sessions are not injected via DI frameworks.

---

## Best Practices

- Use `.transaction()` or `.session()` explicitly in your service-layer or job code
to clearly define execution boundaries.
- `.execute(...)` is ideal for small projects, functional-style code, or early-stage prototypes - it avoids
boilerplate and makes code fast to write.
- As your project grows, you can gradually migrate to DI-based session and transaction management:
just replace `db.execute(...)` with `self._session.execute(...)`
and `db.transaction()` with your own context (e.g., `UnitOfWork`, `session.begin()`) - the query logic remains the same.
- This makes the library especially useful for bootstrapping or background scripts,
where a full-blown DI setup would be overkill.

---

## Tests

```shell
pytest --cov=sqlalchemy_tx_context --cov-report=term-missing
```

---

## Compatibility

Tested on Python `3.9` - `3.12`.

---

## License

MIT License
