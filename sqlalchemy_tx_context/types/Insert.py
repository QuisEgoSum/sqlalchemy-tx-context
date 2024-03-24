from typing import Optional, Any, TypeVar, TYPE_CHECKING, overload, Union

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
from sqlalchemy.sql.dml import ReturningInsert as SqlalchemyReturningInsert

from .Rowcount import Rowcount
from .WithDataMixin import WithDataMixin

T = TypeVar("T")


class ReturningInsert(SqlalchemyReturningInsert[T], WithDataMixin[T], Rowcount):
    pass


# noinspection PyProtectedMember,PyMethodOverriding
class Insert(sqlalchemy.Insert, Rowcount):
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
        # START OVERLOADED FUNCTIONS self.returning ReturningInsert 1-8 ", *, sort_by_parameter_order: bool = False"  # noqa: E501

        # code within this block is **programmatically,
        # statically generated** by tools/generate_tuple_map_overloads.py

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            *,
            sort_by_parameter_order: bool = False
        ) -> ReturningInsert[_T0]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[Union[_T0, _T1]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[Union[_T0, _T1, _T2]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[Union[_T0, _T1, _T2, _T3]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            __ent4: _TypedColumnClauseArgument[_T4],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[Union[_T0, _T1, _T2, _T3, _T4]]: ...

        @overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            __ent4: _TypedColumnClauseArgument[_T4],
            __ent5: _TypedColumnClauseArgument[_T5],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[Union[_T0, _T1, _T2, _T3, _T4, _T5]]: ...

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
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6]]: ...

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
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[
            Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7]
        ]: ...

        # END OVERLOADED FUNCTIONS self.returning

        @overload
        def returning(
            self,
            *cols: _ColumnsClauseArgument[Any],
            sort_by_parameter_order: bool = False,
            **__kw: Any,
        ) -> ReturningInsert[Any]: ...

        def returning(
            self,
            *cols: _ColumnsClauseArgument[Any],
            sort_by_parameter_order: bool = False,
            **__kw: Any,
        ) -> ReturningInsert[Any]: ...
