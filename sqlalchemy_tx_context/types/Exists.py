from typing import Optional, Any

import sqlalchemy
from sqlalchemy import util, Result, CursorResult, UnaryExpression
# noinspection PyProtectedMember
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams
# noinspection PyProtectedMember
from sqlalchemy.orm._typing import OrmExecuteOptionsParameter
# noinspection PyProtectedMember
from sqlalchemy.orm.session import _BindArguments
from sqlalchemy.sql.selectable import Exists as SqlalchemyExists
from typing_extensions import Union

from .Select import Select


class Exists(SqlalchemyExists):
    async def execute(
        self,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None
    ) -> Union[Result, CursorResult]: ...

    def select(self) -> Select[Any]: ...
