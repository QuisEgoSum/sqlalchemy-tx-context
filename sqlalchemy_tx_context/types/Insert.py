import typing
from typing import Optional, Any

import sqlalchemy
from sqlalchemy import util, Result, CursorResult
# noinspection PyProtectedMember
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams
# noinspection PyProtectedMember
from sqlalchemy.orm._typing import OrmExecuteOptionsParameter
# noinspection PyProtectedMember
from sqlalchemy.orm.session import _BindArguments
# noinspection PyProtectedMember
from sqlalchemy.sql._typing import (
    _TP, _TypedColumnClauseArgument,
    _ColumnsClauseArgument,
    _T0, _T1, _T2, _T3,
    _T4, _T5, _T6, _T7
)
from sqlalchemy.sql.dml import ReturningInsert as SqlalchemyReturningInsert
from sqlalchemy.sql.selectable import TypedReturnsRows


class ReturningInsert(SqlalchemyReturningInsert, TypedReturnsRows[_TP]):
    async def execute(
            self,
            params: Optional[_CoreAnyExecuteParams] = None,
            *,
            execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
            bind_arguments: Optional[_BindArguments] = None,
            _parent_execute_state: Optional[Any] = None,
            _add_event: Optional[Any] = None
    ) -> Result[_TP]: ...


# noinspection PyProtectedMember,PyMethodOverriding
class Insert(sqlalchemy.Insert):
    async def execute(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
    ) -> CursorResult[Any]: ...

    if typing.TYPE_CHECKING:
        # START OVERLOADED FUNCTIONS self.returning ReturningInsert 1-8 ", *, sort_by_parameter_order: bool = False"  # noqa: E501

        # code within this block is **programmatically,
        # statically generated** by tools/generate_tuple_map_overloads.py

        @typing.overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            *,
            sort_by_parameter_order: bool = False
        ) -> ReturningInsert[typing.Tuple[_T0]]: ...

        @typing.overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[typing.Tuple[_T0, _T1]]: ...

        @typing.overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[typing.Tuple[_T0, _T1, _T2]]: ...

        @typing.overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[typing.Tuple[_T0, _T1, _T2, _T3]]: ...

        @typing.overload
        def returning(
            self,
            __ent0: _TypedColumnClauseArgument[_T0],
            __ent1: _TypedColumnClauseArgument[_T1],
            __ent2: _TypedColumnClauseArgument[_T2],
            __ent3: _TypedColumnClauseArgument[_T3],
            __ent4: _TypedColumnClauseArgument[_T4],
            *,
            sort_by_parameter_order: bool = False,
        ) -> ReturningInsert[typing.Tuple[_T0, _T1, _T2, _T3, _T4]]: ...

        @typing.overload
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
        ) -> ReturningInsert[typing.Tuple[_T0, _T1, _T2, _T3, _T4, _T5]]: ...

        @typing.overload
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
        ) -> ReturningInsert[typing.Tuple[_T0, _T1, _T2, _T3, _T4, _T5, _T6]]: ...

        @typing.overload
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
            typing.Tuple[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7]
        ]: ...

        # END OVERLOADED FUNCTIONS self.returning

        @typing.overload
        def returning(
            self,
            *cols: _ColumnsClauseArgument[typing.Any],
            sort_by_parameter_order: bool = False,
            **__kw: typing.Any,
        ) -> ReturningInsert[typing.Any]: ...

        def returning(
            self,
            *cols: _ColumnsClauseArgument[typing.Any],
            sort_by_parameter_order: bool = False,
            **__kw: typing.Any,
        ) -> ReturningInsert[typing.Any]: ...
