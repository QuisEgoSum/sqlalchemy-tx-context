from typing import TYPE_CHECKING, overload, Any, Optional, Union, AsyncContextManager

from sqlalchemy import ScalarSelect, SelectBase
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, AsyncSessionTransaction

from .types import Insert, Select, Update, Delete, Exists, CompoundSelect, postgresql

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from sqlalchemy.sql._typing import _ColumnsClauseArgument, _DMLTableArgument, _SelectStatementForCompoundArgument
    # noinspection PyProtectedMember
    from sqlalchemy.sql._typing import (
        _TypedColumnClauseArgument,
        _ColumnsClauseArgument,
        _T0, _T1, _T2, _T3,
        _T4, _T5, _T6, _T7,
        _T8, _T9
    )


class PostgreSQL:
    def insert(self, table: _DMLTableArgument) -> postgresql.Insert: ...


class SQLAlchemyTransactionContext:
    engine: AsyncEngine
    postgresql: PostgreSQL

    def __init__(self, engine: AsyncEngine): ...

    def transaction(
        self,
        session_maker=None
    ) -> AsyncContextManager[Union[AsyncSession, AsyncSessionTransaction]]: ...

    def current_transaction_or_default(self) -> AsyncContextManager[AsyncSession]: ...

    def get_current_transaction(self) -> Optional[AsyncSession]: ...

    async def new_transaction(
        self,
        session_maker=None
    ) -> AsyncContextManager[Union[AsyncSession, AsyncSessionTransaction]]: ...

    @overload
    def select(self, __ent0: _TypedColumnClauseArgument[_T0]) -> Select[_T0]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1]
    ) -> Select[Union[_T0, _T1]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2]
    ) -> Select[Union[_T0, _T1, _T2]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
    ) -> Select[Union[_T0, _T1, _T2, _T3]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
        __ent6: _TypedColumnClauseArgument[_T6],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
        __ent6: _TypedColumnClauseArgument[_T6],
        __ent7: _TypedColumnClauseArgument[_T7],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
        __ent6: _TypedColumnClauseArgument[_T6],
        __ent7: _TypedColumnClauseArgument[_T7],
        __ent8: _TypedColumnClauseArgument[_T8],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
        __ent6: _TypedColumnClauseArgument[_T6],
        __ent7: _TypedColumnClauseArgument[_T7],
        __ent8: _TypedColumnClauseArgument[_T8],
        __ent9: _TypedColumnClauseArgument[_T9],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8, _T9]]: ...


    # END OVERLOADED FUNCTIONS select


    @overload
    def select(
        self,
        *entities: _ColumnsClauseArgument[Any], **__kw: Any
    ) -> Select[Any]: ...

    def select(self, *entities: _ColumnsClauseArgument[Any], **__kw: Any) -> Select[Any]: ...


    def insert(self, table: _DMLTableArgument) -> Insert: ...


    def update(self, table: _DMLTableArgument) -> Update: ...

    def delete(self, table: _DMLTableArgument) -> Delete: ...

    def union(self, *selects: _SelectStatementForCompoundArgument) -> CompoundSelect: ...

    def union_all(self, *selects: _SelectStatementForCompoundArgument) -> CompoundSelect: ...

    def exists(
        self, __argument: Optional[Union[_ColumnsClauseArgument[Any], SelectBase, ScalarSelect[Any]]] = None
    ) -> Exists: ...
