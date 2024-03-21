from typing import Optional, Any

import sqlalchemy
from sqlalchemy import util, Result
from sqlalchemy.sql.selectable import TypedReturnsRows
# noinspection PyProtectedMember
from sqlalchemy.sql._typing import _TP
# noinspection PyProtectedMember
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams
# noinspection PyProtectedMember
from sqlalchemy.orm._typing import OrmExecuteOptionsParameter
# noinspection PyProtectedMember
from sqlalchemy.orm.session import _BindArguments


class Select(sqlalchemy.Select, TypedReturnsRows[_TP]):
    async def execute(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None
    ) -> Result[_TP]: ...
