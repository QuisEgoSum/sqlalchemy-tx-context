import typing
import contextvars
from contextlib import asynccontextmanager

import sqlalchemy
from sqlalchemy import dialects
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSessionTransaction
from sqlalchemy.ext.asyncio import AsyncSession

FIELD_PROPERTIES = frozenset([
    'query',
    'context'
])

IGNORE_PROPERTIES = frozenset([
    'compile',
    'alias',
    'subquery',
    'label',
    'scalar_subquery'
])

EXECUTE_PROPERTIES = frozenset([
    'execute',
    'scalar',
    'scalars',
    'first',
    'all',
    'mapped_first',
    'mapped_one',
    'mapped_all',
    'rowcount'
])

RESULT_PROPERTIES = frozenset([
    'rowcount',
    'first',
    'all'
])

RESULT_MAPPINGS_PROPERTIES = frozenset([
    'mapped_first',
    'mapped_one',
    'mapped_all',
])

RESULT_MAPPINGS_METHODS = {
    'mapped_first': 'first',
    'mapped_one': 'fetchone',
    'mapped_all': 'fetchall'
}


def _execute_query(context: "SQLAlchemyTransactionContext", query, method: str):
    if method in RESULT_PROPERTIES:
        async def executor(*args, **kwargs):
            # noinspection PyArgumentList
            async with context.current_transaction_or_default() as tx:
                result = await tx.execute(query, *args, **kwargs)
                value = getattr(result, method)
                if callable(value):
                    return value()
                return value
    elif method in RESULT_MAPPINGS_PROPERTIES:
        async def executor(*args, **kwargs):
            # noinspection PyArgumentList
            async with context.current_transaction_or_default() as tx:
                result = await tx.execute(query, *args, **kwargs)
                return getattr(result.mappings(), RESULT_MAPPINGS_METHODS[method])()
    else:
        async def executor(*args, **kwargs):
            # noinspection PyArgumentList
            async with context.current_transaction_or_default() as tx:
                return await getattr(tx, method)(query, *args, **kwargs)
    return executor


class ProxyQuery:
    def __init__(self, query, context: "SQLAlchemyTransactionContext"):
        self.query = query
        self.context = context

    def __getattribute__(self, item):
        if item in FIELD_PROPERTIES:
            return object.__getattribute__(self, item)
        elif item in EXECUTE_PROPERTIES:
            return _execute_query(self.context, self.query, item)
        value = object.__getattribute__(self.query, item)
        if item.startswith('_'):
            return value
        if item in IGNORE_PROPERTIES:
            return value
        if not callable(value):
            return value

        def wrapper(*args, **kwargs):
            self.query = value(*args, **kwargs)
            return self
        return wrapper


class PostgreSQL:
    def __init__(self, insert):
        self.insert = insert


class SQLAlchemyTransactionContext:
    def __init__(
        self,
        engine: AsyncEngine,
        *,
        default_session_maker: typing.Callable[
            [], typing.AsyncContextManager[AsyncSession]
        ] = None
    ):
        self.engine = engine
        if default_session_maker is None:
            self.default_session_maker = async_sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            ).begin
        else:
            self.default_session_maker = default_session_maker
        self._transaction_var = contextvars.ContextVar('transactions')

        self.select = self._proxy_sqlalchemy_query_factory(sqlalchemy.select)
        self.insert = self._proxy_sqlalchemy_query_factory(sqlalchemy.insert)
        self.update = self._proxy_sqlalchemy_query_factory(sqlalchemy.update)
        self.delete = self._proxy_sqlalchemy_query_factory(sqlalchemy.delete)
        self.union = self._proxy_sqlalchemy_query_factory(sqlalchemy.union)
        self.union_all = self._proxy_sqlalchemy_query_factory(sqlalchemy.union_all)
        self.exists = self._proxy_sqlalchemy_query_factory(sqlalchemy.exists)
        self.postgresql = PostgreSQL(
            self._proxy_sqlalchemy_query_factory(dialects.postgresql.insert)
        )

    @asynccontextmanager
    async def transaction(
        self,
        session_maker=None
    ) -> typing.AsyncContextManager[typing.Union[AsyncSession, AsyncSessionTransaction]]:
        tx: typing.Optional[AsyncSession] = self._transaction_var.get(None)
        if tx is None:
            if session_maker is None:
                session_maker = self.default_session_maker
            async with session_maker() as tx:
                token = self._transaction_var.set(tx)
                try:
                    yield tx
                finally:
                    self._transaction_var.reset(token)
        else:
            async with tx.begin_nested() as nested_tx:
                yield nested_tx

    @asynccontextmanager
    async def current_transaction_or_default(self):
        tx: typing.Optional[AsyncSession] = self._transaction_var.get(None)
        if tx is not None:
            yield tx
            return
        async with self.default_session_maker() as tx:
            yield tx

    def get_current_transaction(self) -> typing.Optional[AsyncSession]:
        return self._transaction_var.get(None)

    @asynccontextmanager
    async def new_transaction(
        self,
        session_maker=None
    ):
        if session_maker is None:
            session_maker = self.default_session_maker
        async with session_maker() as tx:
            token = self._transaction_var.set(tx)
            try:
                yield tx
            finally:
                self._transaction_var.reset(token)

    def _proxy_sqlalchemy_query_factory(self, method: typing.Any) -> typing.Any:
        def wrapper(*args, **kwargs):
            return ProxyQuery(method(*args, **kwargs), self)
        return wrapper
