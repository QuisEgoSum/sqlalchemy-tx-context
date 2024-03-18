# TODO
import sqlalchemy


class ResultMixin(sqlalchemy.Result):
    async def __call__(self) -> sqlalchemy.Result: ...


class ExecuteMixin:
    exec: ResultMixin
