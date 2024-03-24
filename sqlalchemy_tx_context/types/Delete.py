from typing import Optional, Any, TYPE_CHECKING, overload, Tuple, TypeVar, Union

import sqlalchemy
from sqlalchemy import util, CursorResult
# noinspection PyProtectedMember
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams
# noinspection PyProtectedMember
from sqlalchemy.orm._typing import OrmExecuteOptionsParameter
# noinspection PyProtectedMember
from sqlalchemy.orm.session import _BindArguments
# noinspection PyProtectedMember
from sqlalchemy.sql._typing import (
    _TypedColumnClauseArgument,
    _ColumnsClauseArgument,
    _T0, _T1, _T2, _T3,
    _T4, _T5, _T6, _T7
)
from sqlalchemy.sql.dml import ReturningDelete as SqlalchemyReturningDelete
from sqlalchemy.sql.selectable import TypedReturnsRows

from .Rowcount import Rowcount
from .WithDataMixin import WithDataMixin

_T = TypeVar("_T")


class ReturningDelete(SqlalchemyReturningDelete, TypedReturnsRows[Tuple[_T]], WithDataMixin[_T], Rowcount):
    pass


class Delete(sqlalchemy.Delete, Rowcount):
    async def execute(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
    ) -> CursorResult[Any]: ...

    if TYPE_CHECKING:
        @overload
        def returning(
            self, __ent0: _TypedColumnClauseArgument[_T0]
        ) -> ReturningDelete[_T0]: ...

        @overload
        def returning(
            self, __ent0: _TypedColumnClauseArgument[_T0], __ent1: _TypedColumnClauseArgument[_T1]
        ) -> ReturningDelete[Union[_T0, _T1]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2]
        ) -> ReturningDelete[Union[_T0, _T1, _T2]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
        ) -> ReturningDelete[Union[_T0, _T1, _T2, _T3]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            __ent4: _TypedColumnClauseArgument[_T4],
        ) -> ReturningDelete[Union[_T0, _T1, _T2, _T3, _T4]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            __ent4: _TypedColumnClauseArgument[_T4],
            __ent5: _TypedColumnClauseArgument[_T5],
        ) -> ReturningDelete[Union[_T0, _T1, _T2, _T3, _T4, _T5]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            __ent4: _TypedColumnClauseArgument[_T4],
            __ent5: _TypedColumnClauseArgument[_T5],
            __ent6: _TypedColumnClauseArgument[_T6],
        ) -> ReturningDelete[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            __ent4: _TypedColumnClauseArgument[_T4],
            __ent5: _TypedColumnClauseArgument[_T5],
            __ent6: _TypedColumnClauseArgument[_T6],
            __ent7: _TypedColumnClauseArgument[_T7],
        ) -> ReturningDelete[
            Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7]
        ]: ...

        @overload
        def returning(
            self, *cols: _ColumnsClauseArgument[Any], **__kw: Any
        ) -> ReturningDelete[Any]: ...

        def returning(
            self, *cols: _ColumnsClauseArgument[Any], **__kw: Any
        ) -> ReturningDelete[Any]: ...
