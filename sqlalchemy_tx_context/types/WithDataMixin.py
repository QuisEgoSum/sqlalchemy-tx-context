import typing
from typing import Any, Optional, Sequence, Generic, TypeVar, Union, Tuple

from sqlalchemy import util, RowMapping, ScalarResult, Row
# noinspection PyProtectedMember
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams
# noinspection PyProtectedMember
from sqlalchemy.orm._typing import OrmExecuteOptionsParameter
# noinspection PyProtectedMember
from sqlalchemy.orm.session import _BindArguments

from .ExecuteMixin import ExecuteMixin

T = TypeVar("T")


class WithDataMixin(Generic[T], ExecuteMixin[T]):
    async def first(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None
    ) -> Optional[Row[Tuple[T]]]: ...

    async def all(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None
    ) -> typing.List[Row[Tuple[T]]]: ...

    async def scalar(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        **kw: Any,
    ) -> Optional[T]: ...

    async def scalars(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        **kw: Any,
    ) -> ScalarResult[T]: ...

    async def mapped_first(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None
    ) -> Optional[Union[RowMapping, T]]: ...

    async def mapped_one(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None
    ) -> Optional[Union[RowMapping, T]]: ...

    async def mapped_all(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None
    ) -> Sequence[Union[RowMapping, T]]: ...
