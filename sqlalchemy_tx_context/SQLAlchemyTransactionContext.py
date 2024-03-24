import typing
import contextvars
from contextlib import asynccontextmanager

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


class ProxyQuery:
    def __init__(self, query):
        self.query = query
        self.execute = None

    def __getattribute__(self, item):
        if item == 'query':
            return object.__getattribute__(self, item)
        value = object.__getattribute__(self.query, item)
        if item == 'execute':
            return value
        if not callable(value):
            return value

        def wrapper(*args, **kwargs):
            query = value(*args, **kwargs)
            if not hasattr(query, 'execute'):
                setattr(query, 'execute', self.execute)
            self.query = query
            return self
        return wrapper


class Execute:
    def __init__(self, _context: "SQLAlchemyTransactionContext", proxy_result: typing.Any):
        self.context = _context
        self.proxy_query = proxy_result

    async def _execute_query(self):
        # noinspection PyArgumentList
        async with self.context.get_current_transaction() as tx:
            return await tx.execute(self.proxy_query.query)

    async def __call__(self):
        return await self._execute_query()


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
            result = method(*args, **kwargs)
            proxy_query = ProxyQuery(result)
            execute = Execute(self, proxy_query)
            proxy_query.execute = execute
            setattr(result, 'execute', execute)
            return proxy_query

        return wrapper
