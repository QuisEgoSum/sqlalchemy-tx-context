import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine

from example.connection import engine
from example.models import Base
from example.service import create_and_list_users, update_user_and_rollback


async def init_db(sa_engine: AsyncEngine) -> None:
    async with sa_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main() -> None:
    await init_db(engine)
    await create_and_list_users()
    await update_user_and_rollback()


if __name__ == "__main__":
    asyncio.run(main())
