import typing

import sqlalchemy

from db.context import get_current_transaction
from db.types import ExecuteMixin

T = typing.TypeVar('T')


class Execute:
    def __init__(self, proxy_result):
        self.proxy_query = proxy_result

    async def _execute_query(self):
        async with get_current_transaction() as tx:
            return await tx.execute(self.proxy_query.query)

    async def __call__(self):
        return await self._execute_query()


def _proxy_method_factory(current_result_property: str):
    async def execute(self):
        return getattr(await self._execute_query(), current_result_property)()
    return execute


def _proxy_property_factory(current_result_property: str):
    async def execute(self):
        return getattr(await self._execute_query(), current_result_property)
    return execute


for result_property in dir(sqlalchemy.Result):
    if not result_property.startswith('_'):
        if callable(getattr(sqlalchemy.Result, result_property)):
            setattr(Execute, result_property, _proxy_method_factory(result_property))
        else:
            setattr(Execute, result_property, _proxy_property_factory(result_property))


class ProxyQuery:
    def __init__(self, query):
        self.query = query

    def __getattribute__(self, item):
        if item == 'query':
            return object.__getattribute__(self, item)
        value = object.__getattribute__(self.query, item)
        if item == 'exec':
            return value
        if not callable(value):
            return value

        def wrapper(*args, **kwargs):
            query = value(*args, **kwargs)
            self.query = query
            return self
        return wrapper


def proxy_sqlalchemy_query_factory(method: T) -> typing.Union[T, typing.Type[ExecuteMixin]]:
    def wrapper(*args, **kwargs):
        result = method(*args, **kwargs)
        proxy_query = ProxyQuery(result)
        execute = Execute(proxy_query)
        setattr(result, 'exec', execute)
        return proxy_query
    return wrapper
