from collections.abc import Sequence
from typing import Optional

from sqlalchemy import insert, select, update

from example.connection import db
from example.models import User


async def insert_user(name: str) -> Optional[User]:
    stmt = insert(User).values(name=name).returning(User)
    result = await db.execute(stmt)
    return result.scalar()


async def get_users() -> Sequence[User]:
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_user(user_id: int, name: str) -> None:
    stmt = update(User).where(User.id == user_id).values(name=name)
    await db.execute(stmt)
