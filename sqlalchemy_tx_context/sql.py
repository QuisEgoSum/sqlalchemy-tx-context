from .context import get_current_transaction


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
    def __init__(self, proxy_result):
        self.proxy_query = proxy_result

    async def _execute_query(self):
        async with get_current_transaction() as tx:
            return await tx.execute(self.proxy_query.query)

    async def __call__(self):
        return await self._execute_query()


def proxy_sqlalchemy_query_factory(method):
    def wrapper(*args, **kwargs):
        result = method(*args, **kwargs)
        proxy_query = ProxyQuery(result)
        execute = Execute(proxy_query)
        proxy_query.execute = execute
        setattr(result, 'execute', execute)
        return proxy_query
    return wrapper
