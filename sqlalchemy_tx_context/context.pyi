import typing

from sqlalchemy.ext.asyncio import AsyncSession


def configure(_default_transaction_factory): ...


def transaction(transaction_factor=None) -> typing.AsyncContextManager[AsyncSession]: ...


def get_current_transaction() -> typing.ContextManager[AsyncSession]: ...
