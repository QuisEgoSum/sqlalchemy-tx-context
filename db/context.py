import contextvars
import typing
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

transaction_var = contextvars.ContextVar('transactions')


default_transaction_factory: typing.Callable


def configure(_default_transaction_factory):
    global default_transaction_factory
    default_transaction_factory = _default_transaction_factory


@asynccontextmanager
async def transaction(transaction_factor=None) -> typing.AsyncContextManager[AsyncSession]:
    global default_transaction_factory
    if transaction_factor is None:
        transaction_factor = default_transaction_factory
    async with transaction_factor() as tx:
        tx_list: typing.Optional[list] = transaction_var.get(None)
        if tx_list:
            tx_list.append(tx)
            token = None
        else:
            tx_list = [tx]
            token = transaction_var.set(tx_list)
        try:
            yield tx
        finally:
            if token is not None:
                transaction_var.reset(token)
            else:
                tx_list.remove(tx)


@asynccontextmanager
async def get_current_transaction() -> typing.ContextManager[AsyncSession]:
    tx_list: typing.Optional[typing.List] = transaction_var.get(None)
    if tx_list:
        yield tx_list[-1]
    else:
        global default_transaction_factory
        async with default_transaction_factory() as tx:
            yield tx
