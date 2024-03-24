from typing import Tuple, TypeVar

import sqlalchemy

from .WithDataMixin import WithDataMixin

T = TypeVar("T")


class Select(sqlalchemy.Select[Tuple[T]], WithDataMixin[T]):
    pass
