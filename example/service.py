from example import dao
from example.connection import db


async def create_and_list_users() -> None:
    async with db.transaction():
        await dao.insert_user("Alice")
        await dao.insert_user("Bob")

    async with db.session():
        users = await dao.get_users()
        print("Users after insert:", users)  # noqa: T201


async def update_user_and_rollback() -> None:
    try:
        async with db.transaction():
            await dao.update_user(user_id=1, name="Updated Alice")
            raise RuntimeError("Force rollback")
    except RuntimeError:
        pass

    async with db.session():
        users = await dao.get_users()
        print("Users after rollback attempt:", users)  # noqa: T201
