import typing
import contextvars
from contextlib import asynccontextmanager

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


FIELD_PROPERTIES = frozenset([
    'query',
    'context'
])

EXECUTE_PROPERTIES = frozenset([
    'execute',
    'scalar',
    'scalars'
])


def _execute_query(context: "SQLAlchemyTransactionContext", query, method: str):
    async def executor(*args, **kwargs):
        # noinspection PyArgumentList
        async with context.get_current_transaction() as tx:
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
        if not callable(value):
            return value

        def wrapper(*args, **kwargs):
            query = value(*args, **kwargs)
            self.query = query
            return self
        return wrapper


class SQLAlchemyTransactionContext:
    def __init__(
        self,
        engine: AsyncEngine,
        *,
        default_session_maker: typing.Callable[
            [], typing.AsyncContextManager[AsyncSession]
        ] = None
    ):
        self._engine = engine
        if default_session_maker is None:
            self._session_maker = async_sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False).begin
        else:
            self._session_maker = default_session_maker
        self._transaction_var = contextvars.ContextVar('transactions')

        self.select = self._proxy_sqlalchemy_query_factory(sqlalchemy.select)
        self.insert = self._proxy_sqlalchemy_query_factory(sqlalchemy.insert)
        self.update = self._proxy_sqlalchemy_query_factory(sqlalchemy.update)
        self.delete = self._proxy_sqlalchemy_query_factory(sqlalchemy.delete)
        self.union = self._proxy_sqlalchemy_query_factory(sqlalchemy.union)
        self.union_all = self._proxy_sqlalchemy_query_factory(sqlalchemy.union_all)
        self.exists = self._proxy_sqlalchemy_query_factory(sqlalchemy.exists)

    @asynccontextmanager
    async def transaction(self, _session_maker=None) -> typing.AsyncContextManager[AsyncSession]:
        if _session_maker is None:
            _session_maker = self._session_maker
        async with _session_maker() as tx:
            tx_list: typing.Optional[list] = self._transaction_var.get(None)
            if tx_list:
                tx_list.append(tx)
                token = None
            else:
                tx_list = [tx]
                token = self._transaction_var.set(tx_list)
            try:
                yield tx
            finally:
                if token is not None:
                    self._transaction_var.reset(token)
                else:
                    tx_list.remove(tx)

    @asynccontextmanager
    async def get_current_transaction(self) -> typing.ContextManager[AsyncSession]:
        tx_list: typing.Optional[typing.List] = self._transaction_var.get(None)
        if tx_list:
            yield tx_list[-1]
        else:
            async with self._session_maker() as tx:
                yield tx

    def _proxy_sqlalchemy_query_factory(self, method: typing.Any) -> typing.Any:
        def wrapper(*args, **kwargs):
            query = method(*args, **kwargs)
            return ProxyQuery(query, self)
        return wrapper
