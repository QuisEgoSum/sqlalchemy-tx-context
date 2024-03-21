from typing import TYPE_CHECKING, overload, Tuple, Any, Optional, Union

from sqlalchemy import ScalarSelect, SelectBase

from .context import transaction
from .types import Insert, Select, Update, Delete, Exists, CompoundSelect

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


# TODO: Remove
def configure(_): ...

@overload
def select(__ent0: _TypedColumnClauseArgument[_T0]) -> Select[Tuple[_T0]]: ...


@overload
def select(
    __ent0: _TypedColumnClauseArgument[_T0], __ent1: _TypedColumnClauseArgument[_T1]
) -> Select[Tuple[_T0, _T1]]: ...


@overload
def select(
    __ent0: _TypedColumnClauseArgument[_T0], __ent1: _TypedColumnClauseArgument[_T1], __ent2: _TypedColumnClauseArgument[_T2]
) -> Select[Tuple[_T0, _T1, _T2]]: ...


@overload
def select(
    __ent0: _TypedColumnClauseArgument[_T0],
    __ent1: _TypedColumnClauseArgument[_T1],
    __ent2: _TypedColumnClauseArgument[_T2],
    __ent3: _TypedColumnClauseArgument[_T3],
) -> Select[Tuple[_T0, _T1, _T2, _T3]]: ...


@overload
def select(
    __ent0: _TypedColumnClauseArgument[_T0],
    __ent1: _TypedColumnClauseArgument[_T1],
    __ent2: _TypedColumnClauseArgument[_T2],
    __ent3: _TypedColumnClauseArgument[_T3],
    __ent4: _TypedColumnClauseArgument[_T4],
) -> Select[Tuple[_T0, _T1, _T2, _T3, _T4]]: ...


@overload
def select(
    __ent0: _TypedColumnClauseArgument[_T0],
    __ent1: _TypedColumnClauseArgument[_T1],
    __ent2: _TypedColumnClauseArgument[_T2],
    __ent3: _TypedColumnClauseArgument[_T3],
    __ent4: _TypedColumnClauseArgument[_T4],
    __ent5: _TypedColumnClauseArgument[_T5],
) -> Select[Tuple[_T0, _T1, _T2, _T3, _T4, _T5]]: ...


@overload
def select(
    __ent0: _TypedColumnClauseArgument[_T0],
    __ent1: _TypedColumnClauseArgument[_T1],
    __ent2: _TypedColumnClauseArgument[_T2],
    __ent3: _TypedColumnClauseArgument[_T3],
    __ent4: _TypedColumnClauseArgument[_T4],
    __ent5: _TypedColumnClauseArgument[_T5],
    __ent6: _TypedColumnClauseArgument[_T6],
) -> Select[Tuple[_T0, _T1, _T2, _T3, _T4, _T5, _T6]]: ...


@overload
def select(
    __ent0: _TypedColumnClauseArgument[_T0],
    __ent1: _TypedColumnClauseArgument[_T1],
    __ent2: _TypedColumnClauseArgument[_T2],
    __ent3: _TypedColumnClauseArgument[_T3],
    __ent4: _TypedColumnClauseArgument[_T4],
    __ent5: _TypedColumnClauseArgument[_T5],
    __ent6: _TypedColumnClauseArgument[_T6],
    __ent7: _TypedColumnClauseArgument[_T7],
) -> Select[Tuple[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7]]: ...


@overload
def select(
    __ent0: _TypedColumnClauseArgument[_T0],
    __ent1: _TypedColumnClauseArgument[_T1],
    __ent2: _TypedColumnClauseArgument[_T2],
    __ent3: _TypedColumnClauseArgument[_T3],
    __ent4: _TypedColumnClauseArgument[_T4],
    __ent5: _TypedColumnClauseArgument[_T5],
    __ent6: _TypedColumnClauseArgument[_T6],
    __ent7: _TypedColumnClauseArgument[_T7],
    __ent8: _TypedColumnClauseArgument[_T8],
) -> Select[Tuple[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]: ...


@overload
def select(
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
) -> Select[Tuple[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8, _T9]]: ...


# END OVERLOADED FUNCTIONS select


@overload
def select(
    *entities: _ColumnsClauseArgument[Any], **__kw: Any
) -> Select[Any]: ...

def select(*entities: _ColumnsClauseArgument[Any], **__kw: Any) -> Select[Any]: ...


def insert(table: _DMLTableArgument) -> Insert: ...


def update(table: _DMLTableArgument) -> Update: ...

def delete(table: _DMLTableArgument) -> Delete: ...

def union(*selects: _SelectStatementForCompoundArgument) -> CompoundSelect: ...

def union_all(*selects: _SelectStatementForCompoundArgument) -> CompoundSelect: ...

def exists(
    __argument: Optional[Union[_ColumnsClauseArgument[Any], SelectBase, ScalarSelect[Any]]] = None
) -> Exists: ...
